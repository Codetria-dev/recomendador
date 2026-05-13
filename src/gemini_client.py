"""
Cliente para API Gemini - Recomendacao de Streaming
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

from dotenv import load_dotenv
from google import genai

from src.i18n import (
    STREAMINGS,
    TIPOS_CONTEUDO,
    CRITERIOS,
    GENEROS,
    build_prompt,
)

logger = logging.getLogger(__name__)

load_dotenv()


def _extrair_json(texto: str) -> list[dict[str, Any]]:
    """Extrai JSON da resposta do Gemini, limpando markdown se necessario."""
    texto = texto.strip()

    if texto.startswith("```"):
        linhas = texto.split("\n", 1)
        texto = linhas[1] if len(linhas) > 1 else texto
        if "```" in texto:
            texto = texto.split("```")[0]

    inicio = texto.find("[")
    fim = texto.rfind("]")
    if inicio != -1 and fim != -1:
        texto = texto[inicio : fim + 1]

    return json.loads(texto)


class GeminiClient:
    """Client for Google Gemini API to generate streaming recommendations."""

    def __init__(self) -> None:
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API_KEY nao encontrada no arquivo .env")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    def recomendar(
        self,
        streaming: str,
        tipo: str,
        criterio: str,
        quantidade: int = 8,
        lang: str = "pt",
        genero: str = "",
    ) -> list[dict[str, Any]]:
        """
        Gera recomendacoes usando Gemini API.

        Args:
            streaming: Chave do servico de streaming
            tipo: Tipo de conteudo
            criterio: Criterio de recomendacao
            quantidade: Numero de resultados desejados
            lang: Codigo do idioma (pt, en, fr, zh)
            genero: Filtro de genero (opcional)

        Returns:
            Lista de dicionarios com recomendacoes
        """
        streamings_data = STREAMINGS.get(lang, STREAMINGS["pt"])
        tipos_data = TIPOS_CONTEUDO.get(lang, TIPOS_CONTEUDO["pt"])
        criterios_data = CRITERIOS.get(lang, CRITERIOS["pt"])
        generos_data = GENEROS.get(lang, GENEROS["pt"])

        streaming_nome = streamings_data.get(streaming, streaming)
        tipo_nome = tipos_data.get(tipo, tipo)
        criterio_desc = criterios_data.get(criterio, criterio)
        genero_nome = generos_data.get(genero, "")

        prompt = build_prompt(
            streaming=streaming,
            streaming_nome=streaming_nome,
            tipo_nome=tipo_nome,
            criterio_desc=criterio_desc,
            quantidade=quantidade,
            lang=lang,
            genero_nome=genero_nome,
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            resultados = _extrair_json(response.text)
            logger.info(
                "Gemini [%s] retornou %d recomendacoes para %s/%s/%s",
                lang,
                len(resultados),
                streaming,
                tipo,
                criterio,
            )
            return resultados[:quantidade]

        except Exception as e:
            logger.error("Erro ao chamar Gemini API: %s", e, exc_info=True)
            raise RuntimeError(f"Falha ao gerar recomendacoes: {e}") from e
