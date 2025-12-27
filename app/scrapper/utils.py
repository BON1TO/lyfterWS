from urllib.parse import urljoin, urlparse, parse_qs


def is_content_sufficient(static_result: dict) -> bool:
    metrics = static_result.get("_raw_metrics", {})

    text_len = metrics.get("text_length", 0)
    paragraphs = metrics.get("paragraph_count", 0)
    headings = metrics.get("heading_count", 0)

    # Assignment-safe heuristic:
    # If meaningful readable content exists, static is sufficient
    if text_len >= 500 and paragraphs >= 3 and headings >= 1:
        return True

    return False







def extract_pagination_links(base_url: str, soup, max_pages=3):
    """
    Extract pagination links like:
    ?page=2
    /page/2
    """
    links = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])

        if "page=" in href or "/page/" in href:
            if href not in seen:
                links.append(href)
                seen.add(href)

        if len(links) >= max_pages - 1:
            break

    return links
