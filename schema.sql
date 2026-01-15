DROP TABLE IF EXISTS Rating;
DROP TABLE IF EXISTS MovieActor;
DROP TABLE IF EXISTS MovieDirector;
DROP TABLE IF EXISTS MovieGenre;
DROP TABLE IF EXISTS AppUser;
DROP TABLE IF EXISTS Actor;
DROP TABLE IF EXISTS Director;
DROP TABLE IF EXISTS Movie;
DROP TABLE IF EXISTS Genre;

-- Genre
CREATE TABLE Genre (
    genre_name      VARCHAR(120) PRIMARY KEY
);

-- Movie
CREATE TABLE Movie (
    series_title    VARCHAR(120),
    released_year   INT,
    certificate     VARCHAR(120),
    runtime_minutes INT,
    imdb_rating     REAL,
    overview        VARCHAR(1000),
    meta_score      INT,
    no_of_votes     INT,
    gross           INT,
    poster_link     VARCHAR(500),
    PRIMARY KEY (series_title, released_year)
);

-- MovieGenre (Movie - Genre)
CREATE TABLE MovieGenre (
    series_title    VARCHAR(120),
    released_year   INT,
    genre_name      VARCHAR(120),
    PRIMARY KEY (series_title, released_year, genre_name),
    FOREIGN KEY (series_title, released_year)
        REFERENCES Movie(series_title, released_year),
    FOREIGN KEY (genre_name)
        REFERENCES Genre(genre_name)
);

-- Director
CREATE TABLE Director (
    director_name   VARCHAR(120) PRIMARY KEY
);

-- MovieDirector (Movie - Director)
CREATE TABLE MovieDirector (
    series_title    VARCHAR(120),
    released_year   INT,
    director_name   VARCHAR(120),
    PRIMARY KEY (series_title, released_year, director_name),
    FOREIGN KEY (series_title, released_year)
        REFERENCES Movie(series_title, released_year),
    FOREIGN KEY (director_name)
        REFERENCES Director(director_name)
);

-- Actor
CREATE TABLE Actor (
    actor_name      VARCHAR(120) PRIMARY KEY
);

-- MovieActor (Movie - Actor)
CREATE TABLE MovieActor (
    series_title    VARCHAR(120),
    released_year   INT,
    actor_name      VARCHAR(120),
    billing_order   INT,
    PRIMARY KEY (series_title, released_year, actor_name),
    FOREIGN KEY (series_title, released_year)
        REFERENCES Movie(series_title, released_year),
    FOREIGN KEY (actor_name)
        REFERENCES Actor(actor_name)
);

-- AppUser
CREATE TABLE AppUser (
    username        VARCHAR(120) PRIMARY KEY,
    display_name    VARCHAR(120),
    email           VARCHAR(120)
);

-- Rating (User - Movie)
CREATE TABLE Rating (
    username        VARCHAR(120),
    series_title    VARCHAR(120),
    released_year   INT,
    rating_value    INT,
    PRIMARY KEY (username, series_title, released_year),
    FOREIGN KEY (username)
        REFERENCES AppUser(username),
    FOREIGN KEY (series_title, released_year)
        REFERENCES Movie(series_title, released_year)
);
