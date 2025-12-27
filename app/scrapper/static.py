import httpx
from .utils import extract_pagination_links
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_static(url: str):
    result = {
        "meta": {},
        "content": {
            "headings": [],
            "paragraphs": [],
            "links": [],
            "images": []
        }
    }

    try:
        response = httpx.get(url, timeout=10, follow_redirects=True)
        response.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Static fetch failed: {e}")

    soup = BeautifulSoup(response.text, "lxml")

    # -------- META --------
    title = soup.find("title")
    result["meta"]["title"] = title.text.strip() if title else ""

    description = soup.find("meta", attrs={"name": "description"})
    result["meta"]["description"] = (
        description["content"].strip() if description and "content" in description.attrs else ""
    )

    result["meta"]["language"] = (
    html_tag.get("lang").split("-")[0] if html_tag and html_tag.get("lang") else "en"
)


    canonical = soup.find("link", rel="canonical")
    result["meta"]["canonical"] = canonical.get("href") if canonical else None

    # -------- HEADINGS --------
    for level in range(1, 7):
        for h in soup.find_all(f"h{level}"):
            text = h.get_text(strip=True)
            if text:
                result["content"]["headings"].append({
                    "level": level,
                    "text": text
                })

    # -------- PARAGRAPHS --------
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if text:
            result["content"]["paragraphs"].append(text)

    # -------- LINKS --------
    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"])
        text = a.get_text(strip=True)
        result["content"]["links"].append({
            "text": text,
            "href": href
        })

    # -------- IMAGES --------
    for img in soup.find_all("img", src=True):
        src = urljoin(url, img["src"])
        alt = img.get("alt", "")
        result["content"]["images"].append({
            "src": src,
            "alt": alt
        })

    return result
