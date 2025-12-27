import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

NOISE_SELECTORS = [
    "cookie",
    "consent",
    "modal",
    "popup",
    "overlay",
    "newsletter"
]


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

    # -------- RAW HTML & METRICS (BEFORE NOISE FILTERING) --------
    raw_paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    raw_headings = [
        h.get_text(strip=True)
        for h in soup.find_all(["h1", "h2", "h3"])
    ]

    result["_raw_html"] = response.text
    result["_raw_metrics"] = {
        "text_length": len(" ".join(raw_paragraphs)),
        "paragraph_count": len(raw_paragraphs),
        "heading_count": len(raw_headings),
    }

    # -------- NOISE FILTERING --------
    for el in soup.find_all(True):
        classes = el.get("class")
        class_text = " ".join(classes) if isinstance(classes, list) else ""
        id_text = el.get("id") or ""

        class_id = f"{class_text} {id_text}".lower()

        if any(k in class_id for k in NOISE_SELECTORS):
            el.decompose()


    # -------- META --------
    title = soup.find("title")
    result["meta"]["title"] = title.text.strip() if title else ""

    description = soup.find("meta", attrs={"name": "description"})
    result["meta"]["description"] = (
        description["content"].strip()
        if description and "content" in description.attrs
        else ""
    )

    html_tag = soup.find("html")
    result["meta"]["language"] = (
        html_tag.get("lang").split("-")[0]
        if html_tag and html_tag.get("lang")
        else "en"
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
