from app.scrapper.static import scrape_static
from fastapi.staticfiles import StaticFiles

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
    sections = []
    meta = {}

    try:
        static_data = scrape_static(req.url)

        sections.append({
            "id": "static-main",
            "type": "static",
            "label": "Main Content",
            "content": static_data["content"],
            "rawHtml": None,
            "truncated": False
        })

        meta = static_data["meta"]

    except Exception as e:
        errors.append({
            "phase": "static",
            "message": str(e)
        })

    return {
        "result": {
            "url": req.url,
            "scrapedAt": datetime.utcnow().isoformat() + "Z",
            "meta": meta,
            "sections": sections,
            "interactions": {
                "clicks": [],
                "scrolls": 0,
                "pages": [req.url]
            },
            "errors": errors
        }
    }


    return {"result": result}
