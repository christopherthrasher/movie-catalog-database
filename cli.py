from typing import Optional

from models import AppUser
from services import MovieCatalogService


class CLI:
    def __init__(self, service: MovieCatalogService):
        self.service = service

    def run(self) -> None:
        while True:
            self.show_main_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.handle_view_movies()
            elif choice == "2":
                self.handle_search_by_genre()
            elif choice == "3":
                self.handle_rate_movie()
            elif choice == "4":
                self.handle_view_movie_ratings()
            elif choice.lower() in ("5", "q", "quit", "exit"):
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")

    def show_main_menu(self) -> None:
        print("\n=== Movie Catalog ===")
        print("1) List movies")
        print("2) Search movies by genre")
        print("3) Rate a movie")
        print("4) View ratings for a movie")
        print("5) Exit")

    # Option 1: List movies

    def handle_view_movies(self) -> None:
        try:
            limit_str = input("How many movies to show?: ").strip()
            limit = int(limit_str) if limit_str else 20
        except ValueError:
            print("Invalid number, defaulting to 20.")
            limit = 20

        try:
            movies = self.service.list_all_movies(limit=limit)
        except Exception as e:
            print(f"Error while listing movies: {e}")
            return

        if not movies:
            print("No movies found.")
            return

        print(f"\nShowing up to {len(movies)} movies:\n")
        for idx, movie in enumerate(movies, start=1):
            print(f"{idx}. {movie.get_title()} ({movie.get_released_year()})")

    # Option 2: Search by genre

    def handle_search_by_genre(self) -> None:
        genre_name = input("Enter genre name: ").strip()
        if not genre_name:
            print("Genre name cannot be empty.")
            return

        try:
            movies = self.service.search_by_genre(genre_name, limit=50)
        except Exception as e:
            print(f"Error while searching by genre: {e}")
            return

        if not movies:
            print(f"No movies found for genre: {genre_name}")
            return

        print(f"\nMovies in genre '{genre_name}':\n")
        for idx, movie in enumerate(movies, start=1):
            print(f"{idx}. {movie.get_title()} ({movie.get_released_year()})")

    # Option 3: Rate a movie

    def handle_rate_movie(self) -> None:
        print("\n=== Rate a Movie ===")

        username = input("Enter your username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return
        try:
            user = self.service.get_user(username)
        except Exception as e:
            print(f"Error while fetching user: {e}")
            return

        if user is None:
            print("No user found with that username.")
            create = input("Create a new user with this username? (y/n): ").strip().lower()
            if create != "y":
                print("Rating cancelled.")
                return

            display_name = input("Enter display name: ").strip()
            email = input("Enter email: ").strip()
            user = AppUser(username=username, display_name=display_name, email=email)

            try:
                self.service.add_user(user)
            except Exception as e:
                print(f"Error while creating user: {e}")
                return

            print(f"User '{username}' created.")

        title = input("Enter movie title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return

        try:
            year_str = input("Enter movie release year: ").strip()
            year = int(year_str)
        except ValueError:
            print("Invalid year.")
            return

        try:
            movie = self.service.find_movie(title, year)
        except Exception as e:
            print(f"Error while looking up movie: {e}")
            return

        if movie is None:
            print(f"Movie '{title}' ({year}) not found in the catalog.")
            return

        try:
            rating_str = input("Enter your rating (1–10): ").strip()
            rating_value = int(rating_str)
        except ValueError:
            print("Invalid rating; must be a number.")
            return

        if rating_value < 1 or rating_value > 10:
            print("Rating must be between 1 and 10.")
            return

        review = input("Optional: enter a short review (or leave blank): ").strip()

        # Store rating via service
        try:
            self.service.add_user_rating(
                username=username,
                title=title,
                year=year,
                value=rating_value,
                review=review,
            )
        except Exception as e:
            print(f"Error while saving rating: {e}")
            return

        print(f"Saved rating {rating_value}/10 for '{title}' ({year}) by user '{username}'.")

    # Option 4: View ratings

    def handle_view_movie_ratings(self) -> None:
        print("\n=== View Ratings for a Movie ===")

        title = input("Enter movie title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return

        try:
            year_str = input("Enter movie release year: ").strip()
            year = int(year_str)
        except ValueError:
            print("Invalid year.")
            return

        try:
            movie = self.service.find_movie(title, year)
        except Exception as e:
            print(f"Error while looking up movie: {e}")
            return

        if movie is None:
            print(f"Movie '{title}' ({year}) not found.")
            return

        try:
            ratings = self.service.get_movie_ratings(title, year)
        except Exception as e:
            print(f"Error while fetching ratings: {e}")
            return

        if not ratings:
            print(f"No ratings found for '{title}' ({year}).")
            return

        print(f"\nRatings for '{title}' ({year}):")
        values = [r.get_rating_value() for r in ratings]
        for idx, r in enumerate(ratings, start=1):
            print(f"{idx}. Rating: {r.get_rating_value()}")

        avg = sum(values) / len(values)
        print(f"\nAverage rating: {avg:.2f} based on {len(values)} rating(s).")


if __name__ == "__main__":
    service = MovieCatalogService()
    cli = CLI(service)
    cli.run()
