from bs4 import BeautifulSoup
from lxml import html as lxml_html


def _extract_one(soup: BeautifulSoup, tree, field_config: dict) -> str | None:
    xpath = field_config.get("xpath")
    selector = field_config.get("selector")
    attribute = field_config.get("attribute")

    if xpath:
        results = tree.xpath(xpath)
        if not results:
            return None
        result = results[0]
        if isinstance(result, str):
            return result.strip() or None
        text = result.get(attribute) if attribute else result.text_content()
        return text.strip() if text else None

    if selector:
        node = soup.select_one(selector)
        if node is None:
            return None
        text = node.get(attribute) if attribute else node.get_text(strip=True)
        return text.strip() if isinstance(text, str) else text

    return None


def extract_fields(html: str, config: dict[str, dict]) -> dict[str, str | None]:
    soup = BeautifulSoup(html, "lxml")
    tree = lxml_html.fromstring(html) if html else None

    values: dict[str, str | None] = {}
    for field_name, field_config in config.items():
        values[field_name] = _extract_one(soup, tree, field_config)
    return values


def looks_incomplete(raw_values: dict[str, str | None], config: dict[str, dict]) -> bool:
    if not raw_values:
        return True
    return all(value is None or value == "" for value in raw_values.values())
