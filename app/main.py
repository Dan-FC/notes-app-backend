import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _cors_origins() -> list[str]:
    raw = os.environ.get("CORS_ORIGINS", "")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(title="Notes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_methods=["*"],
    allow_headers=["*"],
)

notes: dict[str, dict] = {}


@app.get("/health")
def health():
    return {"status": "ok"}


class NoteCreate(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class Note(BaseModel):
    id: str
    text: str
    created_at: str


@app.get("/notes", response_model=list[Note])
def list_notes():
    return sorted(notes.values(), key=lambda n: n["created_at"], reverse=True)


@app.post("/notes", response_model=Note, status_code=201)
def create_note(body: NoteCreate):
    note = {
        "id": str(uuid4()),
        "text": body.text.strip(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    notes[note["id"]] = note
    return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: str):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    del notes[note_id]
