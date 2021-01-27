from main import app
from unittest.mock import Mock
import pytest
import json


@pytest.mark.parametrize("list_type", ("top_rated", "upcoming", "popular", "now_playing"))
def test_movies_list(monkeypatch, list_type):
    api_mock = Mock(return_value={"results": []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
