from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import change_events, job_runs, templates, trackers

app = FastAPI(title="Scraping + Tracking Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trackers.router)
app.include_router(change_events.router)
app.include_router(job_runs.router)
app.include_router(templates.router)


@app.get("/health")
def health():
    return {"status": "ok"}
