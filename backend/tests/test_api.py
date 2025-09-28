# backend/tests/test_api.py

# -------------------------------
# API Endpoint Tests
# -------------------------------

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "STAR Library API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert data["database"] in ["connected", "disconnected"]

def test_get_books(client):
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "HP and the Sorcerer's Stone"

def test_get_authors(client):
    response = client.get("/authors/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "J.K. Rowling"

def test_get_reader(client):
    response = client.get("/readers/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice"
    assert "books_read" in data

def test_get_reader_not_found(client):
    response = client.get("/readers/99999")
    assert response.status_code == 404
    assert "detail" in response.json()

def test_dashboard(client):
    response = client.get("/dashboard/1")
    assert response.status_code == 200
    data = response.json()
    assert "most_popular_books" in data
    assert "user_top_authors" in data
    assert "books_read" in data
    assert data["reader_id"] == 1
