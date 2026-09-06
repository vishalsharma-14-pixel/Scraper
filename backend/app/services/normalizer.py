import re

_PRICE_NUMBER_RE = re.compile(r"\d[\d,]*\.\d+|\d[\d,]*")
_NUMBER_RE = re.compile(r"-?\d[\d,]*\.?\d*")
_WHITESPACE_RE = re.compile(r"\s+")

_IN_STOCK_KEYWORDS = ("in stock", "available", "in-stock", "add to cart", "buy now")
_OUT_OF_STOCK_KEYWORDS = ("out of stock", "sold out", "unavailable", "out-of-stock", "notify me")


def normalize_price(raw: str | None) -> float | None:
    if raw is None:
        return None
    # Sites commonly render a price twice in the same element (an accessible
    # off-screen copy alongside visually-split digit spans, e.g. Amazon's
    # `.a-price` markup) — search for the first number instead of requiring
    # the whole cleaned string to parse, so that duplication doesn't corrupt it.
    match = _PRICE_NUMBER_RE.search(raw)
    if not match:
        return None
    try:
        return float(match.group().replace(",", ""))
    except ValueError:
        return None


def normalize_number(raw: str | None) -> float | None:
    if raw is None:
        return None
    match = _NUMBER_RE.search(raw)
    if not match:
        return None
    try:
        return float(match.group().replace(",", ""))
    except ValueError:
        return None


def normalize_text(raw: str | None) -> str | None:
    if raw is None:
        return None
    cleaned = _WHITESPACE_RE.sub(" ", raw).strip()
    return cleaned or None


def normalize_availability(raw: str | None) -> str | None:
    if raw is None:
        return None
    lowered = raw.lower()
    if any(keyword in lowered for keyword in _OUT_OF_STOCK_KEYWORDS):
        return "out_of_stock"
    if any(keyword in lowered for keyword in _IN_STOCK_KEYWORDS):
        return "in_stock"
    return "unknown"


_NORMALIZERS = {
    "price": normalize_price,
    "number": normalize_number,
    "text": normalize_text,
    "availability": normalize_availability,
}


def normalize_value(raw: str | None, field_type: str):
    normalizer = _NORMALIZERS.get(field_type, normalize_text)
    return normalizer(raw)
