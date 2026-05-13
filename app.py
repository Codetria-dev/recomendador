"""
API Flask para Recomendacao de Streaming com Google Gemini.
Suporte multi-idioma: Portugues, English, Francais, 中文.
"""
from __future__ import annotations

import hashlib
import logging
import time
import traceback
from typing import Any

from flask import Flask, render_template, request, jsonify, Response

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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

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
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


def _get_lang() -> str:
    """Extract language from request (query param for GET, body for POST)."""
    if request.method == 'GET':
        return request.args.get('lang', 'pt')
    data = request.get_json(silent=True) or {}
    return data.get('lang', request.args.get('lang', 'pt'))


@app.route('/')
def index() -> str:
    """Renderiza a interface web."""
    return render_template('index.html')


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
