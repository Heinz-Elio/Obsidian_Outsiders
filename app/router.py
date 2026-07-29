from __future__ import annotations


SCOPE_PREFIXES = {
    "characters": "01_character",
    "locations": "02_location",
    "species": "03_species",
    "languages": "04_language",
    "srunes": "05_srune",
    "technology": "06_technology",
    "items": "07_item",
    "organizations": "08_organization",
    "events": "09_event",
    "legends": "10_legend",
    "factions": "11_faction",
}

SCOPE_CATEGORIES = {
    "characters": "character",
    "locations": "location",
    "species": "species",
    "languages": "language",
    "srunes": "srune",
    "technology": "technology",
    "items": "item",
    "organizations": "organization",
    "events": "event",
    "legends": "legend",
    "factions": "faction",
}

SCOPE_ALIASES = {
    "character": "characters",
    "角色": "characters",
    "人物": "characters",
    "location": "locations",
    "地點": "locations",
    "species": "species",
    "種族": "species",
    "language": "languages",
    "語言": "languages",
    "srune": "srunes",
    "法術": "srunes",
    "magic": "srunes",
    "technology": "technology",
    "技術": "technology",
    "item": "items",
    "物品": "items",
    "weapon": "items",
    "武器": "items",
    "organization": "organizations",
    "組織": "organizations",
    "faction": "factions",
    "派系": "factions",
    "event": "events",
    "事件": "events",
    "legend": "legends",
    "傳說": "legends",
}

AUTO_SCOPE_TERMS = {
    "characters": ("角色", "人物", "誰是", "身份", "性格", "character"),
    "locations": ("地點", "王城", "位置", "location"),
    "species": ("種族", "物種", "species"),
    "languages": ("語言", "language"),
    "srunes": ("法術", "術式", "魔法", "srune"),
    "technology": ("技術", "科技", "technology"),
    "items": ("武器", "裝備", "物品", "item"),
    "organizations": ("組織", "機構", "王國", "organization"),
    "events": ("事件", "經歷", "event"),
    "legends": ("傳說", "神話", "legend"),
    "factions": ("派系", "陣營", "faction"),
}


def normalise_scope(scope: str | None) -> str | None:
    if not scope:
        return None
    value = scope.strip().lower()
    value = SCOPE_ALIASES.get(value, value)
    return value if value in SCOPE_CATEGORIES else None


def resolve_scope(query: str, scope: str | None) -> str | None:
    explicit = normalise_scope(scope)
    if scope and explicit is None:
        return None
    if explicit:
        return explicit
    lowered = query.lower()
    matches = [
        name
        for name, terms in AUTO_SCOPE_TERMS.items()
        if any(term.lower() in lowered for term in terms)
    ]
    return matches[0] if len(matches) == 1 else None
