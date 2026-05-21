"""
Cliente para API TMDB - Enriquecimento com posters, notas, elenco, trailers e onde assistir.
"""
from __future__ import annotations

import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
PROFILE_BASE = "https://image.tmdb.org/t/p/w92"
LOGO_BASE = "https://image.tmdb.org/t/p/w45"

_TIPO_TO_MEDIA = {
    "filme": "movie", "curta": "movie", "animacao": "movie",
    "serie": "tv", "documentario": "tv",
}


class TMDBClient:
    """Client for TMDB API with full enrichment: posters, ratings, credits, trailers, watch providers."""

    def __init__(self) -> None:
        self.read_token = os.getenv("TMDB_READ_TOKEN")
        if not self.read_token:
            raise ValueError("TMDB_READ_TOKEN nao encontrado no arquivo .env")

        self.base_url = "https://api.themoviedb.org/3"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.read_token}",
            "Content-Type": "application/json",
        })
        self._cache: dict[str, Any] = {}

    def _search(
        self, query: str, year: int | None = None, media_type: str = "movie"
    ) -> dict[str, Any] | None:
        """Search TMDB for a title."""
        endpoint = f"{self.base_url}/search/{media_type}"
        params: dict[str, Any] = {"query": query, "page": 1}
        if year:
            params["year"] = year

        try:
            resp = self.session.get(endpoint, params=params, timeout=10)
            resp.raise_for_status()
            results = resp.json().get("results", [])
            return results[0] if results else None
        except requests.RequestException as e:
            logger.warning("TMDB search error for '%s': %s", query, e)
        return None

    def _get_details(
        self, tmdb_id: int, media_type: str
    ) -> dict[str, Any] | None:
        """Get full details with credits, videos, and watch providers."""
        endpoint = f"{self.base_url}/{media_type}/{tmdb_id}"
        params = {
            "append_to_response": "credits,videos,watch/providers",
            "language": "pt-BR",
        }
        try:
            resp = self.session.get(endpoint, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            logger.warning("TMDB details error for id %d: %s", tmdb_id, e)
        return None

    def _parse_director(self, crew: list[dict[str, Any]]) -> str:
        """Extract director name from crew list."""
        for member in crew:
            if member.get("job") == "Director":
                return member.get("name", "")
        return ""

    def _parse_cast(self, cast: list[dict[str, Any]], limit: int = 3) -> list[dict[str, str]]:
        """Extract top cast with name and photo."""
        result = []
        for actor in sorted(cast, key=lambda a: a.get("order", 999))[:limit]:
            profile = actor.get("profile_path")
            result.append({
                "nome": actor.get("name", ""),
                "personagem": actor.get("character", ""),
                "foto": f"{PROFILE_BASE}{profile}" if profile else None,
            })
        return result

    def _parse_trailer(self, videos: dict[str, Any]) -> str | None:
        """Extract YouTube trailer key."""
        results = videos.get("results", [])
        for v in results:
            if v.get("site") == "YouTube" and v.get("type") == "Trailer":
                return v.get("key")
        for v in results:
            if v.get("site") == "YouTube" and v.get("type") in ("Teaser", "Clip"):
                return v.get("key")
        return None

    def _parse_watch_providers(
        self, watch_data: dict[str, Any], country: str = "BR"
    ) -> list[dict[str, str]]:
        """Extract flatrate streaming providers for a given country."""
        results = watch_data.get("results", {})
        country_data = results.get(country, results.get("US", {}))
        providers = []
        for p in country_data.get("flatrate", []):
            logo = p.get("logo_path")
            providers.append({
                "nome": p.get("provider_name", ""),
                "logo": f"{LOGO_BASE}{logo}" if logo else None,
            })
        return providers

    def enrich(
        self,
        titulo: str,
        ano: int | None = None,
        content_type: str = "filme",
    ) -> dict[str, Any]:
        """
        Busca dados completos de um titulo na TMDB.

        Returns:
            Dict with poster, ratings, url, director, cast, trailer, watch providers.
        """
        cache_key = f"{titulo}_{ano}_{content_type}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        media_type = _TIPO_TO_MEDIA.get(content_type, "movie")
        result = self._search(titulo, ano, media_type)

        if not result:
            fallback = "tv" if media_type == "movie" else "movie"
            result = self._search(titulo, ano, fallback)
            if result:
                media_type = fallback

        if not result:
            self._cache[cache_key] = {}
            return {}

        tmdb_id = result.get("id")
        poster_path = result.get("poster_path")

        enriched: dict[str, Any] = {
            "tmdb_poster": f"{IMAGE_BASE}{poster_path}" if poster_path else None,
            "tmdb_nota": round(float(result.get("vote_average", 0)), 1),
            "tmdb_url": (
                f"https://www.themoviedb.org/{media_type}/{tmdb_id}"
                if tmdb_id else None
            ),
            "tmdb_diretor": None,
            "tmdb_elenco": [],
            "tmdb_trailer": None,
            "tmdb_provedores": [],
        }

        # Get detailed data with credits, videos, watch providers
        if tmdb_id:
            details = self._get_details(tmdb_id, media_type)
            if details:
                credits = details.get("credits", {})
                enriched["tmdb_diretor"] = self._parse_director(credits.get("crew", []))
                enriched["tmdb_elenco"] = self._parse_cast(credits.get("cast", []))
                enriched["tmdb_trailer"] = self._parse_trailer(details.get("videos", {}))
                enriched["tmdb_provedores"] = self._parse_watch_providers(
                    details.get("watch/providers", {})
                )

        self._cache[cache_key] = enriched
        return enriched

    def enrich_many(
        self,
        resultados: list[dict[str, Any]],
        content_type: str = "filme",
    ) -> list[dict[str, Any]]:
        """Enrich a list of results with full TMDB data."""
        for item in resultados:
            data = self.enrich(
                titulo=item.get("titulo", ""),
                ano=item.get("ano"),
                content_type=content_type,
            )
            item.update(data)
        return resultados

    def clear_cache(self) -> None:
        """Clear the internal cache."""
        self._cache.clear()
