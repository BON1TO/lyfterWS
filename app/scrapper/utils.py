from urllib.parse import urljoin, urlparse, parse_qs


def is_content_sufficient(static_result: dict) -> bool:
    """
    Heuristic to decide whether static scraping is sufficient.
    Assignment-acceptable logic.
    """
    paragraphs = static_result["content"].get("paragraphs", [])
    headings = static_result["content"].get("headings", [])

    if len(paragraphs) < 2:
        return False
    if len(headings) < 1:
        return False

    return True


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
