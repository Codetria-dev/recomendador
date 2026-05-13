"""
Internationalization module for StreamRecomenda.
Supports: Portuguese (pt), English (en), French (fr), Chinese (zh).
"""
from __future__ import annotations

from typing import Any

# Language display names (used in the language selector)
LINGUAS = {
    "pt": "Portugues",
    "en": "English",
    "fr": "Francais",
    "zh": "中文",
}

# --- Streaming service names (brand names are mostly the same across languages) ---
STREAMINGS: dict[str, dict[str, str]] = {
    "pt": {
        "netflix": "Netflix",
        "prime": "Amazon Prime Video",
        "hbo": "HBO Max",
        "disney": "Disney+",
        "apple": "Apple TV+",
        "globoplay": "Globoplay",
    },
    "en": {
        "netflix": "Netflix",
        "prime": "Amazon Prime Video",
        "hbo": "HBO Max",
        "disney": "Disney+",
        "apple": "Apple TV+",
        "globoplay": "Globoplay",
    },
    "fr": {
        "netflix": "Netflix",
        "prime": "Amazon Prime Video",
        "hbo": "HBO Max",
        "disney": "Disney+",
        "apple": "Apple TV+",
        "globoplay": "Globoplay",
    },
    "zh": {
        "netflix": "Netflix",
        "prime": "Amazon Prime Video",
        "hbo": "HBO Max",
        "disney": "Disney+",
        "apple": "Apple TV+",
        "globoplay": "Globoplay",
    },
}

# --- Content type names ---
TIPOS_CONTEUDO: dict[str, dict[str, str]] = {
    "pt": {
        "filme": "Filme",
        "serie": "Serie",
        "documentario": "Documentario",
        "curta": "Curta-metragem",
        "animacao": "Animacao/Anime",
    },
    "en": {
        "filme": "Movie",
        "serie": "Series",
        "documentario": "Documentary",
        "curta": "Short Film",
        "animacao": "Animation/Anime",
    },
    "fr": {
        "filme": "Film",
        "serie": "Serie",
        "documentario": "Documentaire",
        "curta": "Court-metrage",
        "animacao": "Animation/Anime",
    },
    "zh": {
        "filme": "电影",
        "serie": "剧集",
        "documentario": "纪录片",
        "curta": "短片",
        "animacao": "动画/动漫",
    },
}

# --- Criteria descriptions ---
CRITERIOS: dict[str, dict[str, str]] = {
    "pt": {
        "mais_vistos": "Mais assistidos e populares (blockbusters, maiores audiencias)",
        "menos_vistos": "Subestimados e joias escondidas (obras que merecem mais reconhecimento)",
        "mais_premiados": "Mais premiados e aclamados pela critica (Oscar, Emmy, festivais)",
        "mais_buscados": "Mais comentados e trending topics do momento",
    },
    "en": {
        "mais_vistos": "Most watched and popular (blockbusters, highest audiences)",
        "menos_vistos": "Underrated hidden gems (works that deserve more recognition)",
        "mais_premiados": "Most awarded and critically acclaimed (Oscar, Emmy, festivals)",
        "mais_buscados": "Most talked about and trending topics right now",
    },
    "fr": {
        "mais_vistos": "Les plus regardes et populaires (blockbusters, plus grands publics)",
        "menos_vistos": "Perles meconnues et sous-estimees (oeuvres qui meritent plus de reconnaissance)",
        "mais_premiados": "Les plus recompenses et acclaims par la critique (Oscar, Emmy, festivals)",
        "mais_buscados": "Les plus commentes et tendances du moment",
    },
    "zh": {
        "mais_vistos": "最受欢迎和热门（大片，最高收视率）",
        "menos_vistos": "被低估的隐藏瑰宝（值得更多认可的作品）",
        "mais_premiados": "获奖最多且广受好评（奥斯卡、艾美奖、电影节）",
        "mais_buscados": "当下最热门和 trending 话题",
    },
}

# --- Genre names ---
GENEROS: dict[str, dict[str, str]] = {
    "pt": {
        "acao": "Acao",
        "comedia": "Comedia",
        "drama": "Drama",
        "terror": "Terror",
        "ficcao": "Ficcao Cientifica",
        "romance": "Romance",
        "suspense": "Suspense",
        "animacao": "Animacao",
        "fantasia": "Fantasia",
        "musical": "Musical",
        "guerra": "Guerra",
        "faroeste": "Faroeste",
        "misterio": "Misterio",
    },
    "en": {
        "acao": "Action",
        "comedia": "Comedy",
        "drama": "Drama",
        "terror": "Horror",
        "ficcao": "Sci-Fi",
        "romance": "Romance",
        "suspense": "Thriller",
        "animacao": "Animation",
        "fantasia": "Fantasy",
        "musical": "Musical",
        "guerra": "War",
        "faroeste": "Western",
        "misterio": "Mystery",
    },
    "fr": {
        "acao": "Action",
        "comedia": "Comedie",
        "drama": "Drame",
        "terror": "Horreur",
        "ficcao": "Sci-Fi",
        "romance": "Romance",
        "suspense": "Thriller",
        "animacao": "Animation",
        "fantasia": "Fantaisie",
        "musical": "Comedie musicale",
        "guerra": "Guerre",
        "faroeste": "Western",
        "misterio": "Mystere",
    },
    "zh": {
        "acao": "动作",
        "comedia": "喜剧",
        "drama": "剧情",
        "terror": "恐怖",
        "ficcao": "科幻",
        "romance": "爱情",
        "suspense": "惊悚",
        "animacao": "动画",
        "fantasia": "奇幻",
        "musical": "音乐剧",
        "guerra": "战争",
        "faroeste": "西部",
        "misterio": "悬疑",
    },
}

# --- UI text strings ---
UI: dict[str, dict[str, str]] = {
    "pt": {
        "site_title": "StreamRecomenda - Recomendacoes de Streaming",
        "logo_subtitle": "Recomendacoes inteligentes para seu streaming",
        "hero_title": "O que assistir hoje?",
        "hero_desc": "Escolha seu servico de streaming, o tipo de conteudo e o criterio. Nossa IA recomenda os melhores titulos para voce.",
        "label_streaming": "Servico de Streaming",
        "label_tipo": "Tipo de Conteudo",
        "label_criterio": "Criterio",
        "label_genero": "Genero",
        "select_placeholder": "Selecione...",
        "btn_recommend": "Recomendar",
        "btn_recommending": "Recomendando...",
        "loading_text": "Consultando a inteligencia artificial...",
        "results_title": "Recomendacoes {streaming} — {tipo}",
        "results_count": "{n} resultados",
        "genre_fallback": "Variado",
        "label_nota_ia": "Nota IA",
        "label_nota_tmdb": "Nota TMDB",
        "label_ver_tmdb": "Ver na TMDB",
        "label_sem_poster": "Sem imagem",
        "label_nota_trakt": "Trakt",
        "label_votos_trakt": "votos",
        "label_ver_trakt": "Ver na Trakt",
        "label_diretor": "Diretor",
        "label_elenco": "Elenco",
        "label_trailer": "Trailer",
        "label_onde_assistir": "Onde assistir",
        "label_compartilhar": "Compartilhar",
        "label_favoritar": "Favoritar",
        "label_remover_favoritos": "Remover dos favoritos",
        "btn_nova_recomendacao": "Nova recomendacao",
        "label_historico": "Historico",
        "label_sem_historico": "Nenhuma consulta ainda",
        "label_favoritos": "Favoritos",
        "label_sem_favoritos": "Nenhum favorito ainda",
        "label_compartilhado": "Link copiado!",
        "error_default": "Erro ao gerar recomendacoes",
        "error_connection": "Erro de conexao: {msg}",
        "error_empty": "Nenhum resultado encontrado para esses criterios.",
        "empty_title": "Pronto para descobrir algo novo?",
        "empty_desc": "Selecione suas preferencias e clique em Recomendar.",
        "footer": "StreamRecomenda — Recomendacoes inteligentes com Google Gemini",
    },
    "en": {
        "site_title": "StreamRecomenda - Streaming Recommendations",
        "logo_subtitle": "Smart recommendations for your streaming",
        "hero_title": "What to watch today?",
        "hero_desc": "Choose your streaming service, content type, and criteria. Our AI recommends the best titles for you.",
        "label_streaming": "Streaming Service",
        "label_tipo": "Content Type",
        "label_criterio": "Criteria",
        "label_genero": "Genre",
        "select_placeholder": "Select...",
        "btn_recommend": "Recommend",
        "btn_recommending": "Recommending...",
        "loading_text": "Querying artificial intelligence...",
        "results_title": "Recommendations {streaming} — {tipo}",
        "results_count": "{n} results",
        "genre_fallback": "Various",
        "label_nota_ia": "AI Score",
        "label_nota_tmdb": "TMDB Score",
        "label_ver_tmdb": "View on TMDB",
        "label_sem_poster": "No image",
        "label_nota_trakt": "Trakt",
        "label_votos_trakt": "votes",
        "label_ver_trakt": "View on Trakt",
        "label_diretor": "Director",
        "label_elenco": "Cast",
        "label_trailer": "Trailer",
        "label_onde_assistir": "Where to watch",
        "label_compartilhar": "Share",
        "label_favoritar": "Favorite",
        "label_remover_favoritos": "Remove from favorites",
        "btn_nova_recomendacao": "New recommendation",
        "label_historico": "History",
        "label_sem_historico": "No searches yet",
        "label_favoritos": "Favorites",
        "label_sem_favoritos": "No favorites yet",
        "label_compartilhado": "Link copied!",
        "error_default": "Error generating recommendations",
        "error_connection": "Connection error: {msg}",
        "error_empty": "No results found for these criteria.",
        "empty_title": "Ready to discover something new?",
        "empty_desc": "Select your preferences and click Recommend.",
        "footer": "StreamRecomenda — Smart recommendations with Google Gemini",
    },
    "fr": {
        "site_title": "StreamRecomenda - Recommandations de Streaming",
        "logo_subtitle": "Recommandations intelligentes pour votre streaming",
        "hero_title": "Que regarder aujourd'hui?",
        "hero_desc": "Choisissez votre service de streaming, le type de contenu et le critere. Notre IA recommande les meilleurs titres pour vous.",
        "label_streaming": "Service de Streaming",
        "label_tipo": "Type de Contenu",
        "label_criterio": "Critere",
        "label_genero": "Genre",
        "select_placeholder": "Selectionnez...",
        "btn_recommend": "Recommander",
        "btn_recommending": "Recommandation en cours...",
        "loading_text": "Consultation de l'intelligence artificielle...",
        "results_title": "Recommandations {streaming} — {tipo}",
        "results_count": "{n} resultats",
        "genre_fallback": "Divers",
        "label_nota_ia": "Note IA",
        "label_nota_tmdb": "Note TMDB",
        "label_ver_tmdb": "Voir sur TMDB",
        "label_sem_poster": "Pas d'image",
        "label_nota_trakt": "Trakt",
        "label_votos_trakt": "votes",
        "label_ver_trakt": "Voir sur Trakt",
        "label_diretor": "Realisateur",
        "label_elenco": "Casting",
        "label_trailer": "Bande-annonce",
        "label_onde_assistir": "Ou regarder",
        "label_compartilhar": "Partager",
        "label_favoritar": "Favoris",
        "label_remover_favoritos": "Retirer des favoris",
        "btn_nova_recomendacao": "Nouvelle recommandation",
        "label_historico": "Historique",
        "label_sem_historico": "Aucune recherche",
        "label_favoritos": "Favoris",
        "label_sem_favoritos": "Aucun favori",
        "label_compartilhado": "Lien copie !",
        "error_default": "Erreur lors de la generation des recommandations",
        "error_connection": "Erreur de connexion : {msg}",
        "error_empty": "Aucun resultat trouve pour ces criteres.",
        "empty_title": "Pret a decouvrir quelque chose de nouveau?",
        "empty_desc": "Selectionnez vos preferences et cliquez sur Recommander.",
        "footer": "StreamRecomenda — Recommandations intelligentes avec Google Gemini",
    },
    "zh": {
        "site_title": "StreamRecomenda - 流媒体推荐",
        "logo_subtitle": "为您的流媒体提供智能推荐",
        "hero_title": "今天看什么？",
        "hero_desc": "选择您的流媒体服务、内容类型和标准。我们的人工智能为您推荐最佳影片。",
        "label_streaming": "流媒体服务",
        "label_tipo": "内容类型",
        "label_criterio": "筛选标准",
        "label_genero": "类型",
        "select_placeholder": "请选择...",
        "btn_recommend": "推荐",
        "btn_recommending": "正在推荐...",
        "loading_text": "正在查询人工智能...",
        "results_title": "推荐 {streaming} — {tipo}",
        "results_count": "{n} 个结果",
        "genre_fallback": "综合",
        "label_nota_ia": "AI 评分",
        "label_nota_tmdb": "TMDB 评分",
        "label_ver_tmdb": "在TMDB上查看",
        "label_sem_poster": "暂无图片",
        "label_nota_trakt": "Trakt",
        "label_votos_trakt": "票",
        "label_ver_trakt": "在Trakt上查看",
        "label_diretor": "导演",
        "label_elenco": "演员",
        "label_trailer": "预告片",
        "label_onde_assistir": "观看平台",
        "label_compartilhar": "分享",
        "label_favoritar": "收藏",
        "label_remover_favoritos": "取消收藏",
        "btn_nova_recomendacao": "新推荐",
        "label_historico": "历史记录",
        "label_sem_historico": "暂无搜索记录",
        "label_favoritos": "收藏夹",
        "label_sem_favoritos": "暂无收藏",
        "label_compartilhado": "链接已复制！",
        "error_default": "生成推荐时出错",
        "error_connection": "连接错误: {msg}",
        "error_empty": "未找到符合这些条件的结果。",
        "empty_title": "准备好发现新内容了吗？",
        "empty_desc": "选择您的偏好，然后点击推荐。",
        "footer": "StreamRecomenda — 基于 Google Gemini 的智能推荐",
    },
}

# --- API error messages ---
ERROS: dict[str, dict[str, str]] = {
    "pt": {
        "invalid_streaming": "Servico de streaming invalido. Opcoes: {opcoes}",
        "invalid_tipo": "Tipo de conteudo invalido. Opcoes: {opcoes}",
        "invalid_criterio": "Criterio invalido. Opcoes: {opcoes}",
        "invalid_genero": "Genero invalido. Opcoes: {opcoes}",
        "api_error": "Erro ao gerar recomendacoes. Verifique sua chave API.",
    },
    "en": {
        "invalid_streaming": "Invalid streaming service. Options: {opcoes}",
        "invalid_tipo": "Invalid content type. Options: {opcoes}",
        "invalid_criterio": "Invalid criteria. Options: {opcoes}",
        "invalid_genero": "Invalid genre. Options: {opcoes}",
        "api_error": "Error generating recommendations. Check your API key.",
    },
    "fr": {
        "invalid_streaming": "Service de streaming invalide. Options : {opcoes}",
        "invalid_tipo": "Type de contenu invalide. Options : {opcoes}",
        "invalid_criterio": "Critere invalide. Options : {opcoes}",
        "invalid_genero": "Genre invalide. Options : {opcoes}",
        "api_error": "Erreur lors de la generation des recommandations. Verifiez votre cle API.",
    },
    "zh": {
        "invalid_streaming": "无效的流媒体服务。选项: {opcoes}",
        "invalid_tipo": "无效的内容类型。选项: {opcoes}",
        "invalid_criterio": "无效的筛选标准。选项: {opcoes}",
        "invalid_genero": "无效的类型。选项: {opcoes}",
        "api_error": "生成推荐时出错。请检查您的 API 密钥。",
    },
}

# --- Gemini prompt templates ---
PROMPTS: dict[str, str] = {
    "pt": (
        "Voce e um especialista em recomendar filmes, series e documentarios.\n\n"
        "Com base nos criterios abaixo, recomende {quantidade} titulos disponiveis no streaming informado:\n\n"
        "Servico de Streaming: {streaming_nome}\n"
        "Tipo de Conteudo: {tipo_nome}\n"
        "Criterio: {criterio_desc}\n\n"
        "REGRAS IMPORTANTES:\n"
        "- Responda APENAS com um JSON valido, sem markdown, sem ```json\n"
        "- Use exatamente este formato (array de objetos):\n"
        '[\n'
        '  {{\n'
        '    "titulo": "Nome do Titulo",\n'
        '    "ano": 2024,\n'
        '    "sinopse": "Breve descricao da trama (maximo 2 linhas)",\n'
        '    "nota": 8.5,\n'
        '    "genero": "genero principal",\n'
        '    "destaque": "Por que este titulo se encaixa no criterio"\n'
        '  }}\n'
        "]\n\n"
        "REGRAS:\n"
        "- Nota deve ser entre 0 e 10 (uma casa decimal)\n"
        "- Ano deve ser inteiro\n"
        "- Garanta que os titulos realmente existam no catalogo atual do streaming\n"
        "- Varie os generos dentro do tipo escolhido\n"
        "- Destaque deve explicar a relevancia para o criterio selecionado\n"
        "IMPORTANTE: responda EM PORTUGUES."
    ),
    "en": (
        "You are an expert at recommending movies, series, and documentaries.\n\n"
        "Based on the criteria below, recommend {quantidade} titles available on the given streaming service:\n\n"
        "Streaming Service: {streaming_nome}\n"
        "Content Type: {tipo_nome}\n"
        "Criteria: {criterio_desc}\n\n"
        "IMPORTANT RULES:\n"
        "- Respond ONLY with valid JSON, no markdown, no ```json\n"
        "- Use exactly this format (array of objects):\n"
        '[\n'
        '  {{\n'
        '    "titulo": "Title Name",\n'
        '    "ano": 2024,\n'
        '    "sinopse": "Brief plot description (max 2 lines)",\n'
        '    "nota": 8.5,\n'
        '    "genero": "main genre",\n'
        '    "destaque": "Why this title fits the criteria"\n'
        '  }}\n'
        "]\n\n"
        "RULES:\n"
        "- Rating must be between 0 and 10 (one decimal place)\n"
        "- Year must be an integer\n"
        "- Ensure titles actually exist in the streaming service's current catalog\n"
        "- Vary genres within the chosen content type\n"
        "- Destaque should explain relevance to the selected criteria\n"
        "IMPORTANT: respond IN ENGLISH."
    ),
    "fr": (
        "Vous etes un expert en recommandation de films, series et documentaires.\n\n"
        "Sur la base des criteres ci-dessous, recommandez {quantidade} titres disponibles sur le service de streaming indique :\n\n"
        "Service de Streaming : {streaming_nome}\n"
        "Type de Contenu : {tipo_nome}\n"
        "Critere : {criterio_desc}\n\n"
        "REGLES IMPORTANTES :\n"
        "- Repondez UNIQUEMENT avec un JSON valide, sans markdown, sans ```json\n"
        "- Utilisez exactement ce format (tableau d'objets) :\n"
        '[\n'
        '  {{\n'
        '    "titulo": "Nom du Titre",\n'
        '    "ano": 2024,\n'
        '    "sinopse": "Brève description de l\'intrigue (max 2 lignes)",\n'
        '    "nota": 8.5,\n'
        '    "genero": "genre principal",\n'
        '    "destaque": "Pourquoi ce titre correspond au critere"\n'
        '  }}\n'
        "]\n\n"
        "REGLES :\n"
        "- La note doit etre entre 0 et 10 (un decimal)\n"
        "- L'annee doit etre un entier\n"
        "- Assurez-vous que les titres existent reellement dans le catalogue actuel du service\n"
        "- Variez les genres dans le type de contenu choisi\n"
        "- Destaque doit expliquer la pertinence par rapport au critere selectionne\n"
        "IMPORTANT : repondez EN FRANCAIS."
    ),
    "zh": (
        "您是推荐电影、剧集和纪录片的专家。\n\n"
        "根据以下条件，推荐 {quantidade} 部在指定流媒体服务上可观看的影片：\n\n"
        "流媒体服务: {streaming_nome}\n"
        "内容类型: {tipo_nome}\n"
        "标准: {criterio_desc}\n\n"
        "重要规则:\n"
        "- 仅用有效的 JSON 回复，不要使用 markdown，不要使用 ```json\n"
        "- 使用以下确切格式（对象数组）：\n"
        '[\n'
        '  {{\n'
        '    "titulo": "标题名称",\n'
        '    "ano": 2024,\n'
        '    "sinopse": "简要剧情描述（最多2行）",\n'
        '    "nota": 8.5,\n'
        '    "genero": "主要类型",\n'
        '    "destaque": "为什么这个标题符合标准"\n'
        '  }}\n'
        "]\n\n"
        "规则:\n"
        "- 评分必须在 0 到 10 之间（一位小数）\n"
        "- 年份必须是整数\n"
        "- 确保影片确实存在于该流媒体服务的当前目录中\n"
        "- 在所选择的内容类型中变化类型\n"
        "- 突出显示应解释与所选标准的相关性\n"
        "重要: 用中文回复。"
    ),
}


# --- Utility functions ---

def t(key: str, lang: str = "pt", **kwargs: Any) -> str:
    """Get a translation string by key and language."""
    translation = UI.get(lang, UI["pt"]).get(key, key)
    if kwargs:
        translation = translation.format(**kwargs)
    return translation


def get_error(key: str, lang: str = "pt", **kwargs: Any) -> str:
    """Get an error message by key and language."""
    msg = ERROS.get(lang, ERROS["pt"]).get(key, key)
    if kwargs:
        msg = msg.format(**kwargs)
    return msg


def get_ui_strings(lang: str = "pt") -> dict[str, str]:
    """Return all UI strings for the given language."""
    return UI.get(lang, UI["pt"]).copy()


def get_select_options(lang: str = "pt") -> dict[str, list[dict[str, str]]]:
    """Return translated select options for the frontend."""
    streamings_data = STREAMINGS.get(lang, STREAMINGS["pt"])
    tipos_data = TIPOS_CONTEUDO.get(lang, TIPOS_CONTEUDO["pt"])
    criterios_data = CRITERIOS.get(lang, CRITERIOS["pt"])

    # Criteria names (human-readable in each language)
    criterios_names = {
        "pt": {
            "mais_vistos": "Mais Vistos",
            "menos_vistos": "Menos Vistos",
            "mais_premiados": "Mais Premiados",
            "mais_buscados": "Mais Buscados",
        },
        "en": {
            "mais_vistos": "Most Watched",
            "menos_vistos": "Least Known",
            "mais_premiados": "Most Awarded",
            "mais_buscados": "Most Searched",
        },
        "fr": {
            "mais_vistos": "Les Plus Vus",
            "menos_vistos": "Moins Connus",
            "mais_premiados": "Les Plus Recompenses",
            "mais_buscados": "Les Plus Recherches",
        },
        "zh": {
            "mais_vistos": "最受欢迎",
            "menos_vistos": "冷门佳作",
            "mais_premiados": "获奖最多",
            "mais_buscados": "最热搜",
        },
    }
    cnames = criterios_names.get(lang, criterios_names["pt"])

    generos_data = GENEROS.get(lang, GENEROS["pt"])

    return {
        "streamings": [
            {"id": k, "nome": v} for k, v in streamings_data.items()
        ],
        "tipos": [
            {"id": k, "nome": v} for k, v in tipos_data.items()
        ],
        "criterios": [
            {"id": k, "nome": cnames.get(k, k), "descricao": v}
            for k, v in criterios_data.items()
        ],
        "generos": [
            {"id": k, "nome": v} for k, v in generos_data.items()
        ],
    }


_LABEL_GENERO_PROMPT = {
    "pt": "Genero",
    "en": "Genre",
    "fr": "Genre",
    "zh": "类型",
}

def build_prompt(
    streaming: str,
    streaming_nome: str,
    tipo_nome: str,
    criterio_desc: str,
    quantidade: int = 8,
    lang: str = "pt",
    genero_nome: str = "",
) -> str:
    """Build a Gemini prompt in the requested language."""
    template = PROMPTS.get(lang, PROMPTS["pt"])
    prompt = template.format(
        streaming_nome=streaming_nome,
        tipo_nome=tipo_nome,
        criterio_desc=criterio_desc,
        quantidade=quantidade,
    )
    if genero_nome:
        label = _LABEL_GENERO_PROMPT.get(lang, "Genre")
        prompt += f"\n{label}: {genero_nome}\n"
    return prompt


def get_language_name(lang: str) -> str:
    """Get the display name of a language in itself."""
    return LINGUAS.get(lang, lang)


def supported_languages() -> list[dict[str, str]]:
    """Return list of supported languages."""
    return [
        {"id": k, "nome": v} for k, v in LINGUAS.items()
    ]
