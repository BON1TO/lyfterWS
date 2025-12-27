from app.scrapper.static import scrape_static
from fastapi.staticfiles import StaticFiles
from app.scrapper.utils import is_content_sufficient
from app.scrapper.js import scrape_js
from app.scrapper.sections import split_into_sections

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime

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
    "scrolls": 3,
    "pages": [
        req.url,
        f"{req.url}?page=2",
        f"{req.url}?page=3"
    ]
}


    final_data = None
    mode = None

    # 1️⃣ Try static scraping first
    try:
        static_data = scrape_static(req.url)

        if is_content_sufficient(static_data):
            final_data = static_data
            mode = "static"
        else:
            raise ValueError("Static content insufficient")

    except Exception as e:
        # Log static failure but DO NOT stop
        errors.append({
            "phase": "static",
            "message": str(e)
        })

    # 2️⃣ JS fallback (only if needed)
    if final_data is None:
        try:
            final_data = scrape_js(req.url)
            mode = "js"
        except Exception as e:
            errors.append({
                "phase": "js",
                "message": str(e)
            })

    # 3️⃣ Prepare response
    if final_data:
        sections = split_into_sections(final_data["content"], req.url)

        meta = final_data["meta"]
        meta["mode"] = mode
    else:
        sections = []
        meta = {}

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




    return {"result": result}
