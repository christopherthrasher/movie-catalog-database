from typing import List, Optional
from datetime import datetime

from db_connection import get_connection
from models import Movie, AppUser, Rating


class MovieCatalogService:
    def __init__(self):
        pass

    # Helper methods

    def _row_to_movie(self, row) -> Movie:
        return Movie(
            title=row[0],
            released_year=row[1],
            certificate=row[2],
            runtime_minutes=row[3],
            imdb_rating=row[4],
            overview=row[5],
            meta_score=row[6],
            no_of_votes=row[7],
            gross=row[8],
            poster_link=row[9],
        )

    def _row_to_rating(self, row) -> Rating:
        rating_value, review_text, rated_at = row
        if rated_at is None:
            rated_at = datetime.now()
        return Rating(
            rating_value=rating_value,
            review_text=review_text or "",
            rated_at=rated_at,
        )

    # Movie-related operations

    def list_all_movies(self, limit: int = 50) -> List[Movie]:
        movies: List[Movie] = []

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT series_title,
                           released_year,
                           certificate,
                           runtime_minutes,
                           imdb_rating,
                           overview,
                           meta_score,
                           no_of_votes,
                           gross,
                           poster_link
                    FROM Movie
                    ORDER BY released_year DESC, series_title
                    LIMIT %s;
                    """,
                    (limit,),
                )
                rows = cur.fetchall()

        for row in rows:
            movies.append(self._row_to_movie(row))

        return movies

    def find_movie(self, title: str, year: int) -> Optional[Movie]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT series_title,
                           released_year,
                           certificate,
                           runtime_minutes,
                           imdb_rating,
                           overview,
                           meta_score,
                           no_of_votes,
                           gross,
                           poster_link
                    FROM Movie
                    WHERE series_title = %s
                      AND released_year = %s;
                    """,
                    (title, year),
                )
                row = cur.fetchone()

        if row is None:
            return None

        return self._row_to_movie(row)

    def search_by_genre(self, genre_name: str, limit: int = 50) -> List[Movie]:
        movies: List[Movie] = []

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT m.series_title,
                           m.released_year,
                           m.certificate,
                           m.runtime_minutes,
                           m.imdb_rating,
                           m.overview,
                           m.meta_score,
                           m.no_of_votes,
                           m.gross,
                           m.poster_link
                    FROM Movie m
                    JOIN MovieGenre mg
                      ON m.series_title = mg.series_title
                     AND m.released_year = mg.released_year
                    WHERE mg.genre_name ILIKE %s
                    ORDER BY m.released_year DESC, m.series_title
                    LIMIT %s;
                    """,
                    (genre_name, limit),
                )
                rows = cur.fetchall()

        for row in rows:
            movies.append(self._row_to_movie(row))

        return movies

    # User-related operations

    def add_user(self, user: AppUser) -> None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO AppUser (username, display_name, email)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (username) DO UPDATE
                    SET display_name = EXCLUDED.display_name,
                        email = EXCLUDED.email;
                    """,
                    (user.get_username(), user.get_display_name(), user.get_email()),
                )
            conn.commit()

    def get_user(self, username: str) -> Optional[AppUser]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT username, display_name, email
                    FROM AppUser
                    WHERE username = %s;
                    """,
                    (username,),
                )
                row = cur.fetchone()

        if row is None:
            return None

        return AppUser(username=row[0], display_name=row[1] or "", email=row[2] or "")

    # Rating-related operations

    def add_user_rating(
        self,
        username: str,
        title: str,
        year: int,
        value: int,
        review: str,
    ) -> None:
        # Rating range (1–10)
        if value < 1:
            value = 1
        if value > 10:
            value = 10

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO Rating (username, series_title, released_year, rating_value)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (username, series_title, released_year) DO UPDATE
                    SET rating_value = EXCLUDED.rating_value;
                    """,
                    (username, title, year, value),
                )
            conn.commit()

    def get_movie_ratings(self, title: str, year: int) -> List[Rating]:
        ratings: List[Rating] = []

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT rating_value,
                           '' AS review_text,
                           NULL::timestamp AS rated_at
                    FROM Rating
                    WHERE series_title = %s
                      AND released_year = %s
                    ORDER BY rating_value DESC;
                    """,
                    (title, year),
                )
                rows = cur.fetchall()

        for row in rows:
            ratings.append(self._row_to_rating(row))

        return ratings
