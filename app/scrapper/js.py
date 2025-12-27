from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_js(url: str):
    result = {
        "meta": {},
        "content": {
            "headings": [],
            "paragraphs": [],
            "links": [],
            "images": []
        }
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000, wait_until="domcontentloaded")

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "lxml")

    # -------- META --------
    title = soup.find("title")
    result["meta"]["title"] = title.text.strip() if title else ""

    description = soup.find("meta", attrs={"name": "description"})
    result["meta"]["description"] = (
        description["content"].strip() if description and "content" in description.attrs else ""
    )

    html_tag = soup.find("html")
    result["meta"]["language"] = html_tag.get("lang") if html_tag else ""

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
