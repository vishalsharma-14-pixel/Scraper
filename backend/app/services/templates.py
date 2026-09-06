TEMPLATES = [
    {
        "key": "generic_ecommerce_product",
        "name": "Generic E-commerce Product",
        "description": "Starter selectors for a typical product page: price, title, availability. "
        "Edit the selectors to match the actual site's markup. On pages with 'related "
        "products' or 'customers also bought' carousels, a wildcard class match like "
        "[class*='price'] can grab an unrelated item's price instead of this product's — "
        "scope the selector to a specific container id if that happens (see the Amazon "
        "Product template for an example).",
        "extraction_config": {
            "title": {"selector": "h1", "type": "text"},
            "price": {"selector": ".price, .price-now", "type": "price"},
            "availability": {
                "selector": "#availability span, #availability, .availability",
                "type": "availability",
            },
        },
    },
    {
        "key": "amazon_product",
        "name": "Amazon Product",
        "description": "Selectors scoped to Amazon's product-page wrapper (#ppd), which "
        "avoids the false matches you get from Amazon's 'customers also bought' carousels "
        "when using unscoped wildcard selectors — those carousels reuse the same "
        "price/availability classes as the real product, just for unrelated items. Amazon "
        "varies its price container by layout (#centerCol vs #rightCol) across categories "
        "and regions, so this scopes to the outer #ppd wrapper that contains both.",
        "extraction_config": {
            "title": {"selector": "#productTitle, h1", "type": "text"},
            "price": {
                "selector": "#ppd .a-price .a-offscreen, #ppd .a-price",
                "type": "price",
            },
            "availability": {
                "selector": "#ppd #availability span, #ppd #availability",
                "type": "availability",
            },
        },
    },
    {
        "key": "generic_job_listing",
        "name": "Generic Job Listing",
        "description": "Starter selectors for a job posting page: title, company, status "
        "(e.g. open/closed).",
        "extraction_config": {
            "title": {"selector": "h1", "type": "text"},
            "company": {"selector": ".company, [class*='company']", "type": "text"},
            "status": {"selector": ".job-status, [class*='status']", "type": "text"},
        },
    },
    {
        "key": "generic_article",
        "name": "Generic News/Blog Article",
        "description": "Starter selectors for a news or blog page: headline and byline/date, "
        "useful for detecting edits to a published article.",
        "extraction_config": {
            "headline": {"selector": "h1", "type": "text"},
            "byline": {"selector": ".byline, [class*='author'], time", "type": "text"},
        },
    },
]


def get_templates() -> list[dict]:
    return TEMPLATES
