"""
API Flask para Recomendacao de Streaming com Google Gemini.
Suporte multi-idioma: Portugues, English, Francais, 中文.
"""
from __future__ import annotations

import hashlib
import logging
import os
import time
import traceback
from collections import defaultdict
from typing import Any

from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response

from src.gemini_client import GeminiClient, STREAMINGS, TIPOS_CONTEUDO, CRITERIOS
from src.i18n import GENEROS
from src.tmdb_client import TMDBClient
from src.trakt_client import TraktClient
from src.i18n import (
    get_error,
    get_ui_strings,
    get_select_options,
    supported_languages,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Security: request size limit (1MB) ---
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# --- Rate limiting (simple in-memory per-IP) ---
_RATE_LIMIT_WINDOW = 60       # 60 seconds
_RATE_LIMIT_MAX = 30          # max requests per window
_RATE_LIMIT_BURST = 60        # max burst
_requests: dict[str, list[float]] = defaultdict(list)

# --- CORS origins permitidos ---
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
# Em producao, configure via env: CORS_ORIGINS=https://meu-site.vercel.app,https://meu-dominio.com


def _check_rate_limit(ip: str) -> bool:
    """Verifica se o IP excedeu o limite de requisicoes."""
    now = time.time()
    window_start = now - _RATE_LIMIT_WINDOW

    # Limpar entradas antigas
    _requests[ip] = [t for t in _requests[ip] if t > window_start]

    # Verificar limite
    count = len(_requests[ip])
    if count >= _RATE_LIMIT_MAX:
        # Permitir burst curto
        if count >= _RATE_LIMIT_BURST:
            return False
        # Se estourou o limite normal, verificar se passou tempo suficiente
        if _requests[ip] and (now - _requests[ip][0]) < _RATE_LIMIT_WINDOW:
            return False

    _requests[ip].append(now)
    return True


def _validar_chaves() -> None:
    """Valida que as chaves de API necessarias existem."""
    obrigatorias = {
        "API_KEY": "Google Gemini",
    }
    opcionais = {
        "TMDB_API_KEY": "TMDB (posters, notas)",
        "TMDB_READ_TOKEN": "TMDB (leitura)",
        "TRAKT_CLIENT_ID": "Trakt (votos comunidade)",
    }

    faltando = []
    for chave, nome in obrigatorias.items():
        if not os.getenv(chave):
            faltando.append(f"{chave} ({nome})")

    if faltando:
        logger.warning("Chaves obrigatorias faltando: %s", ", ".join(faltando))
        logger.warning("A API nao funcionara corretamente sem essas chaves.")

    for chave, nome in opcionais.items():
        if not os.getenv(chave):
            logger.info("Chave opcional %s (%s) nao configurada", chave, nome)


# Validar chaves na inicializacao
_validar_chaves()

cliente_gemini: GeminiClient | None = None
cliente_tmdb: TMDBClient | None = None
cliente_trakt: TraktClient | None = None

# Cache simples para recomendacoes (TTL 30 min)
_cache_recomendacoes: dict[str, tuple[float, Any]] = {}
CACHE_TTL = 30 * 60  # 30 minutos


def _cache_key(*args: str) -> str:
    return hashlib.md5("|".join(args).encode()).hexdigest()


def _cache_get(key: str) -> Any | None:
    entry = _cache_recomendacoes.get(key)
    if entry and time.time() - entry[0] < CACHE_TTL:
        return entry[1]
    if entry:
        del _cache_recomendacoes[key]
    return None


def _cache_set(key: str, value: Any) -> None:
    _cache_recomendacoes[key] = (time.time(), value)


def get_gemini_client() -> GeminiClient:
    global cliente_gemini
    if cliente_gemini is None:
        cliente_gemini = GeminiClient()
    return cliente_gemini


def get_tmdb_client() -> TMDBClient | None:
    global cliente_tmdb
    if cliente_tmdb is None:
        try:
            cliente_tmdb = TMDBClient()
        except ValueError:
            logger.warning("TMDB nao configurado - pulando enriquecimento")
    return cliente_tmdb


def get_trakt_client() -> TraktClient | None:
    global cliente_trakt
    if cliente_trakt is None:
        try:
            cliente_trakt = TraktClient()
        except ValueError:
            logger.warning("Trakt nao configurado - pulando enriquecimento")
    return cliente_trakt


@app.after_request
def after_request(response: Response) -> Response:
    origin = request.headers.get('Origin', '')
    # Se a origin estiver na lista permitida, refletir; senao, usar a primeira
    if origin in CORS_ORIGINS or '*' in CORS_ORIGINS:
        response.headers.add('Access-Control-Allow-Origin', origin if origin else '*')
    else:
        response.headers.add('Access-Control-Allow-Origin', CORS_ORIGINS[0] if CORS_ORIGINS[0] else '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


@app.before_request
def before_request() -> Response | None:
    """Rate limiting + log para todas as requisicoes."""
    # Ignorar OPTIONS (preflight CORS)
    if request.method == 'OPTIONS':
        return None

    ip = request.remote_addr or 'desconhecido'
    logger.info("[%s] %s %s", ip, request.method, request.path)

    # Aplicar rate limit apenas em endpoints da API
    if request.path in ('/recomendar', '/dados'):
        if not _check_rate_limit(ip):
            logger.warning("[%s] Rate limit excedido", ip)
            return jsonify({'erro': 'Muitas requisicoes. Tente novamente em alguns segundos.'}), 429

    return None


@app.errorhandler(413)
def request_entity_too_large(_err: Any) -> tuple[Response, int]:
    return jsonify({'erro': 'Requisicao muito grande. Limite de 1MB.'}), 413


def _get_lang() -> str:
    """Extract language from request (query param for GET, body for POST)."""
    if request.method == 'GET':
        return request.args.get('lang', 'pt')
    data = request.get_json(silent=True) or {}
    return data.get('lang', request.args.get('lang', 'pt'))


@app.route('/')
def index() -> tuple[Response, int]:
    """Health check."""
    return jsonify({"status": "ok", "app": "StreamRecomenda API"}), 200


@app.route('/dados')
def dados() -> tuple[Response, int]:
    """
    Retorna dados de configuracao (streamings, tipos, criterios) + UI + idiomas.

    Query params:
        lang: codigo do idioma (pt, en, fr, zh)
    """
    lang = _get_lang()
    if lang not in ("pt", "en", "fr", "zh"):
        lang = "pt"

    return jsonify({
        "linguas": supported_languages(),
        "lingua_atual": lang,
        "ui": get_ui_strings(lang),
        **get_select_options(lang),
    }), 200


@app.route('/recomendar', methods=['POST'])
def recomendar() -> tuple[Response, int]:
    """
    Endpoint para gerar recomendacoes via Gemini.

    Request Body (JSON):
        {
            "streaming": "netflix",
            "tipo": "filme",
            "criterio": "mais_vistos",
            "quantidade": 8 (opcional),
            "lang": "pt" (opcional)
        }
    """
    lang = _get_lang()

    try:
        data: dict[str, Any] = request.get_json() or {}

        streaming = data.get('streaming', '').strip()
        tipo = data.get('tipo', '').strip()
        criterio = data.get('criterio', '').strip()
        genero = data.get('genero', '').strip()
        quantidade = min(int(data.get('quantidade', 8)), 12)

        streamings_data = STREAMINGS.get(lang, STREAMINGS["pt"])
        tipos_data = TIPOS_CONTEUDO.get(lang, TIPOS_CONTEUDO["pt"])
        criterios_data = CRITERIOS.get(lang, CRITERIOS["pt"])
        generos_data = GENEROS.get(lang, GENEROS["pt"])

        if not streaming or streaming not in streamings_data:
            return jsonify({
                'erro': get_error("invalid_streaming", lang, opcoes=", ".join(streamings_data.keys()))
            }), 400

        if not tipo or tipo not in tipos_data:
            return jsonify({
                'erro': get_error("invalid_tipo", lang, opcoes=", ".join(tipos_data.keys()))
            }), 400

        if not criterio or criterio not in criterios_data:
            return jsonify({
                'erro': get_error("invalid_criterio", lang, opcoes=", ".join(criterios_data.keys()))
            }), 400

        if genero and genero not in generos_data:
            return jsonify({
                'erro': get_error("invalid_genero", lang, opcoes=", ".join(generos_data.keys()))
            }), 400

        # Verificar cache
        ck = _cache_key(streaming, tipo, criterio, genero, str(quantidade), lang)
        resultados = _cache_get(ck)

        if resultados is None:
            cliente = get_gemini_client()
            resultados = cliente.recomendar(streaming, tipo, criterio, quantidade, lang, genero)
            _cache_set(ck, resultados)
            logger.info("Cache: MISS para %s/%s/%s/%s", streaming, tipo, criterio, genero or "-")
        else:
            logger.info("Cache: HIT para %s/%s/%s/%s", streaming, tipo, criterio, genero or "-")

        # Enriquecer com dados da TMDB (posters, notas, links)
        tmdb = get_tmdb_client()
        if tmdb:
            try:
                tmdb.enrich_many(resultados, content_type=tipo)
            except Exception as e:
                logger.warning("Erro ao enriquecer com TMDB: %s", e)

        # Enriquecer com dados da Trakt (votos da comunidade)
        trakt = get_trakt_client()
        if trakt:
            try:
                trakt.enrich_many(resultados, content_type=tipo)
            except Exception as e:
                logger.warning("Erro ao enriquecer com Trakt: %s", e)

        logger.info(
            "Recomendacao [%s]: %s/%s/%s - %d resultados",
            lang, streaming, tipo, criterio, len(resultados),
        )

        filtros = {
            'streaming': streamings_data[streaming],
            'tipo': tipos_data[tipo],
            'criterio': criterios_data[criterio],
        }
        if genero:
            filtros['genero'] = generos_data[genero]

        return jsonify({
            'sucesso': True,
            'resultados': resultados,
            'total': len(resultados),
            'filtros': filtros,
        }), 200

    except ValueError as e:
        logger.warning("Erro de validacao: %s", e)
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        logger.error("Erro ao recomendar: %s", traceback.format_exc())
        return jsonify({'erro': get_error("api_error", lang)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("RECOMENDADOR DE STREAMING - API")
    print("=" * 50)
    print("  Idiomas: Portugues, English, Francais, zh")
    print("  Interface: http://localhost:5000")
    print("  API:       POST /recomendar")
    print("=" * 50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
