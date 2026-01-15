import csv
from pathlib import Path

from db_connection import get_connection


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "movies.csv"


def parse_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_runtime(runtime_str):
    if not runtime_str:
        return None
    parts = runtime_str.split()
    for p in parts:
        if p.isdigit():
            return int(p)
    return None


def parse_gross(gross_str):
    if not gross_str:
        return None
    cleaned = "".join(ch for ch in gross_str if ch.isdigit())
    if cleaned == "":
        return None
    return int(cleaned)


def split_genres(genre_str):
    if not genre_str:
        return []
    return [g.strip() for g in genre_str.split(",") if g.strip()]


def main():
    if not DATA_PATH.exists():
        print(f"Could not find CSV at {DATA_PATH}")
        return

    conn = get_connection()
    conn.autocommit = False
    cur = conn.cursor()

    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        count_movies = 0

        for row in reader:
            title = row.get("Series_Title")
            year = parse_int(row.get("Released_Year"))
            certificate = row.get("Certificate")
            runtime_minutes = parse_runtime(row.get("Runtime"))
            imdb_rating = parse_float(row.get("IMDB_Rating"))
            overview = row.get("Overview")
            meta_score = parse_int(row.get("Meta_score"))
            no_of_votes = parse_int(row.get("No_of_Votes"))
            gross = parse_gross(row.get("Gross"))
            poster_link = row.get("Poster_Link")

            if not title or year is None:
                continue

            # 1) Insert Movie
            cur.execute(
                """
                INSERT INTO Movie (
                    series_title, released_year, certificate,
                    runtime_minutes, imdb_rating, overview,
                    meta_score, no_of_votes, gross, poster_link
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (series_title, released_year) DO NOTHING;
                """,
                (
                    title,
                    year,
                    certificate,
                    runtime_minutes,
                    imdb_rating,
                    overview,
                    meta_score,
                    no_of_votes,
                    gross,
                    poster_link,
                ),
            )

            # 2) Genres - Genre + MovieGenre
            for genre_name in split_genres(row.get("Genre")):
                cur.execute(
                    """
                    INSERT INTO Genre (genre_name)
                    VALUES (%s)
                    ON CONFLICT (genre_name) DO NOTHING;
                    """,
                    (genre_name,),
                )

                cur.execute(
                    """
                    INSERT INTO MovieGenre (series_title, released_year, genre_name)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (series_title, released_year, genre_name) DO NOTHING;
                    """,
                    (title, year, genre_name),
                )

            # 3) Director - Director + MovieDirector
            director_name = row.get("Director")
            if director_name:
                cur.execute(
                    """
                    INSERT INTO Director (director_name)
                    VALUES (%s)
                    ON CONFLICT (director_name) DO NOTHING;
                    """,
                    (director_name,),
                )

                cur.execute(
                    """
                    INSERT INTO MovieDirector (series_title, released_year, director_name)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (series_title, released_year, director_name) DO NOTHING;
                    """,
                    (title, year, director_name),
                )

            # 4) Actors - Actor + MovieActor
            stars = [
                row.get("Star1"),
                row.get("Star2"),
                row.get("Star3"),
                row.get("Star4"),
            ]

            for order, actor_name in enumerate(stars, start=1):
                if actor_name and actor_name.strip():
                    actor_name = actor_name.strip()

                    cur.execute(
                        """
                        INSERT INTO Actor (actor_name)
                        VALUES (%s)
                        ON CONFLICT (actor_name) DO NOTHING;
                        """,
                        (actor_name,),
                    )

                    cur.execute(
                        """
                        INSERT INTO MovieActor (series_title, released_year, actor_name, billing_order)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (series_title, released_year, actor_name) DO UPDATE
                        SET billing_order = EXCLUDED.billing_order;
                        """,
                        (title, year, actor_name, order),
                    )

            count_movies += 1

        conn.commit()
        cur.close()
        conn.close()

        print(f"Imported approximately {count_movies} movies from {DATA_PATH.name}.")


if __name__ == "__main__":
    main()
