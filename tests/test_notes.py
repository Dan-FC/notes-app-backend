def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_notes_empty(client):
    response = client.get("/notes")
    assert response.status_code == 200
    assert response.json() == []


def test_create_note(client):
    response = client.post("/notes", json={"text": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Buy milk"
    assert data["id"]
    assert data["created_at"]


def test_create_note_strips_whitespace(client):
    response = client.post("/notes", json={"text": "  trimmed  "})
    assert response.json()["text"] == "trimmed"


def test_create_note_rejects_empty_text(client):
    response = client.post("/notes", json={"text": ""})
    assert response.status_code == 422


def test_list_notes_newest_first(client):
    client.post("/notes", json={"text": "older"})
    client.post("/notes", json={"text": "newer"})

    response = client.get("/notes")
    items = response.json()

    assert len(items) == 2
    assert items[0]["text"] == "newer"
    assert items[1]["text"] == "older"


def test_delete_note(client):
    created = client.post("/notes", json={"text": "remove me"}).json()

    response = client.delete(f"/notes/{created['id']}")
    assert response.status_code == 204
    assert client.get("/notes").json() == []


def test_delete_note_not_found(client):
    response = client.delete("/notes/missing-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"
