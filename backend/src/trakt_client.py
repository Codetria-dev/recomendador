"""
Cliente para API Trakt - Enriquecimento de recomendacoes com votos da comunidade.
"""
from __future__ import annotations

import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


class TraktClient:
    """Client for Trakt API to enrich recommendations with community ratings."""

    def __init__(self) -> None:
        self.client_id = os.getenv("TRAKT_CLIENT_ID")
        if not self.client_id:
            raise ValueError("TRAKT_CLIENT_ID nao encontrado no arquivo .env")

        self.base_url = "https://api.trakt.tv"
        self.session = requests.Session()
        self.session.headers.update({
            "trakt-api-key": self.client_id,
            "trakt-api-version": "2",
            "Content-Type": "application/json",
        })
        self.cache: dict[str, Any] = {}

    def _search(
        self, query: str, year: int | None = None, media_type: str = "movie"
    ) -> dict[str, Any] | None:
        """Search Trakt for a title."""
        endpoint = f"{self.base_url}/search/{media_type}"
        params: dict[str, Any] = {"query": query, "extended": "full"}
        if year:
            params["fields"] = "title,year"

        try:
            resp = self.session.get(endpoint, params=params, timeout=10)
            resp.raise_for_status()
            results = resp.json()

            if not results:
                return None

            # Find best match: prefer exact year or take the first result
            for item in results:
                media = item.get(media_type, {})
                if year and media.get("year") == year:
                    return media
                if not year:
                    return media

            # Fallback to first result if year filter didn't match
            first = results[0]
            return first.get(media_type, {})

        except requests.RequestException as e:
            logger.warning("Trakt search error for '%s': %s", query, e)

        return None

    def enrich(
        self,
        titulo: str,
        ano: int | None = None,
        content_type: str = "filme",
    ) -> dict[str, Any]:
        """
        Busca dados de um titulo na Trakt.

        Returns:
            Dict with trakt_nota, trakt_votos, trakt_url, or empty dict if not found.
        """
        cache_key = f"trakt_{titulo}_{ano}_{content_type}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Map content type to Trakt search type
        if content_type in ("filme", "curta", "animacao"):
            media_type = "movie"
        else:
            media_type = "show"

        result = self._search(titulo, ano, media_type)

        # Fallback: try the other type
        if not result:
            fallback = "show" if media_type == "movie" else "movie"
            result = self._search(titulo, ano, fallback)

        if not result:
            self.cache[cache_key] = {}
            return {}

        ids = result.get("ids", {})

        enriched = {
            "trakt_nota": round(float(result.get("rating", 0)), 1) if result.get("rating") else None,
            "trakt_votos": result.get("votes", 0),
            "trakt_url": (
                f"https://trakt.tv/{media_type}s/{ids.get('slug', ids.get('trakt'))}"
                if ids.get("slug") or ids.get("trakt") else None
            ),
        }

        self.cache[cache_key] = enriched
        return enriched

    def enrich_many(
        self,
        resultados: list[dict[str, Any]],
        content_type: str = "filme",
    ) -> list[dict[str, Any]]:
        """Enrich a list of recommendation results with Trakt data."""
        for item in resultados:
            trakt_data = self.enrich(
                titulo=item.get("titulo", ""),
                ano=item.get("ano"),
                content_type=content_type,
            )
            item.update(trakt_data)
        return resultados
