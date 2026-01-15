# Domain model classes for Movie Catalog

from datetime import datetime
from typing import Optional, List


class Genre:
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def __repr__(self):
        return f"Genre(name='{self._name}')"


class Director:
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def __repr__(self):
        return f"Director(name='{self._name}')"


class Actor:
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def __repr__(self):
        return f"Actor(name='{self._name}')"


class AppUser:
    def __init__(self, username: str, display_name: str, email: str):
        self._username = username
        self._display_name = display_name
        self._email = email
        self._ratings: List[Rating] = []

    def add_rating(self, rating: "Rating") -> None:
        self._ratings.append(rating)

    def get_username(self) -> str:
        return self._username

    def get_display_name(self) -> str:
        return self._display_name

    def get_email(self) -> str:
        return self._email

    def get_ratings(self) -> List["Rating"]:
        return self._ratings

    def __repr__(self):
        return f"AppUser(username='{self._username}', display_name='{self._display_name}', email='{self._email}')"


class Rating:
    def __init__(self, rating_value: int, review_text: str, rated_at: Optional[datetime] = None):
        self._rating_value = rating_value
        self._review_text = review_text
        self._rated_at = rated_at if rated_at else datetime.now()

    def get_rating_value(self) -> int:
        return self._rating_value

    def get_review_text(self) -> str:
        return self._review_text

    def get_rated_at(self) -> datetime:
        return self._rated_at

    def __repr__(self):
        return f"Rating(value={self._rating_value}, review='{self._review_text}', rated_at={self._rated_at})"


class Movie:
    def __init__(
        self,
        title: str,
        released_year: int,
        certificate: Optional[str] = None,
        runtime_minutes: Optional[int] = None,
        imdb_rating: Optional[float] = None,
        overview: Optional[str] = None,
        meta_score: Optional[int] = None,
        no_of_votes: Optional[int] = None,
        gross: Optional[int] = None,
        poster_link: Optional[str] = None,
    ):
        self._title = title
        self._released_year = released_year
        self._certificate = certificate
        self._runtime_minutes = runtime_minutes
        self._imdb_rating = imdb_rating
        self._overview = overview
        self._meta_score = meta_score
        self._no_of_votes = no_of_votes
        self._gross = gross
        self._poster_link = poster_link

        self._genres: List[Genre] = []
        self._directors: List[Director] = []
        self._actors: List[Actor] = []
        self._ratings: List[Rating] = []

    # --- Add methods ---
    def add_genre(self, genre: Genre) -> None:
        self._genres.append(genre)

    def add_director(self, director: Director) -> None:
        self._directors.append(director)

    def add_actor(self, actor: Actor) -> None:
        self._actors.append(actor)

    def add_rating(self, rating: Rating) -> None:
        self._ratings.append(rating)

    # --- Getters ---
    def get_title(self) -> str:
        return self._title

    def get_released_year(self) -> int:
        return self._released_year

    def get_average_rating(self) -> float:
        if not self._ratings:
            return 0.0
        total = sum(r.get_rating_value() for r in self._ratings)
        return round(total / len(self._ratings), 2)

    def __repr__(self):
        return f"Movie(title='{self._title}', year={self._released_year}, imdb={self._imdb_rating})"
