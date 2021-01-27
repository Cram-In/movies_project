import tmdb_client
from unittest.mock import Mock
from tmdb_client import call_tmdb_api


def test_get_poster_url_uses_default_size():
    # Przygotowanie danych
    poster_api_path = "https://image.tmdb.org/t/p/"
    expected_default_size = "w342"
    # Wywołanie kodu, który testujemy
    poster_url = tmdb_client.get_poster_url(poster_api_path=poster_api_path)
    # Porównanie wyników
    assert expected_default_size in poster_url


def test_get_movies_list_type_popular():
    movies_list = tmdb_client.get_movies_list(list_type="popular")
    assert movies_list is not None


def test_get_single_movie(monkeypatch):
    mock_single_movie = "Pomidor"
    single_movie_mock = Mock()
    single_movie_mock.return_value = mock_single_movie
    monkeypatch.setattr("tmdb_client.get_single_movie", single_movie_mock)
    single_movie = tmdb_client.get_single_movie(550)
    assert single_movie == mock_single_movie


def test_get_single_movie_cast(monkeypatch):
    mock_single_movie_cast = "Pomidor"
    cast_single_movie_mock = Mock()
    cast_single_movie_mock.return_value = mock_single_movie_cast
    monkeypatch.setattr("tmdb_client.get_single_movie", cast_single_movie_mock)
    single_movie_cast = tmdb_client.get_single_movie(550)
    assert single_movie_cast == mock_single_movie_cast


def test_get_movie_images(monkeypatch):
    mock_movie_images = "Pomidor.jpg"
    movie_images_mock = Mock()
    movie_images_mock.return_value = mock_movie_images
    monkeypatch.setattr("tmdb_client.get_movie_images", movie_images_mock)
    movie_images = tmdb_client.get_movie_images(550)
    assert movie_images == mock_movie_images