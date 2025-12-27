from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime

from app.scrapper.static import scrape_static
from app.scrapper.js import scrape_js
from app.scrapper.utils import is_content_sufficient
from app.scrapper.sections import split_into_sections

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


class ScrapeRequest(BaseModel):
    url: str


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/scrape")
def scrape(req: ScrapeRequest):
    errors = []
    interactions = {
        "clicks": [],
        "scrolls": 0,
        "pages": [req.url]
    }

    # 1️⃣ Try static scraping first
    try:
        static_data = scrape_static(req.url)

        if is_content_sufficient(static_data):
            final_data = static_data
            mode = "static"
        else:
            raise ValueError("Static content insufficient")

    except Exception as e:
        errors.append({
            "phase": "static",
            "message": str(e)
        })

        # 2️⃣ JS fallback
        try:
            final_data = scrape_js(req.url)
            mode = "js"
        except Exception as je:
            errors.append({
                "phase": "js",
                "message": str(je)
            })
            final_data = {"meta": {}, "content": {}}
            mode = "error"

    # 3️⃣ Split into sections
    sections = split_into_sections(final_data.get("content", {}), req.url)


    # 4️⃣ Meta
    meta = final_data.get("meta", {})
    meta["mode"] = mode

    return {
        "result": {
            "url": req.url,
            "scrapedAt": datetime.utcnow().isoformat() + "Z",
            "meta": meta,
            "sections": sections,
            "interactions": interactions,
            "errors": errors
        }
    }
