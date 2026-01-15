--
-- PostgreSQL database dump
--

\restrict kocDwYcvUAAdFYG4VqStEudQRnkjnoPM5dyAThbVZ0kJnABpfXBTdS2vrwdycea

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2025-12-02 14:48:28

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 224 (class 1259 OID 16934)
-- Name: actor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actor (
    actor_name character varying(120) NOT NULL
);


ALTER TABLE public.actor OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16958)
-- Name: appuser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appuser (
    username character varying(120) NOT NULL,
    display_name character varying(120),
    email character varying(120)
);


ALTER TABLE public.appuser OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16910)
-- Name: director; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.director (
    director_name character varying(120) NOT NULL
);


ALTER TABLE public.director OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16877)
-- Name: genre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.genre (
    genre_name character varying(120) NOT NULL
);


ALTER TABLE public.genre OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16883)
-- Name: movie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie (
    series_title character varying(120) NOT NULL,
    released_year integer NOT NULL,
    certificate character varying(120),
    runtime_minutes integer,
    imdb_rating real,
    overview character varying(1000),
    meta_score integer,
    no_of_votes integer,
    gross integer,
    poster_link character varying(500)
);


ALTER TABLE public.movie OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16940)
-- Name: movieactor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movieactor (
    series_title character varying(120) NOT NULL,
    released_year integer NOT NULL,
    actor_name character varying(120) NOT NULL,
    billing_order integer
);


ALTER TABLE public.movieactor OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16916)
-- Name: moviedirector; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.moviedirector (
    series_title character varying(120) NOT NULL,
    released_year integer NOT NULL,
    director_name character varying(120) NOT NULL
);


ALTER TABLE public.moviedirector OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16892)
-- Name: moviegenre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.moviegenre (
    series_title character varying(120) NOT NULL,
    released_year integer NOT NULL,
    genre_name character varying(120) NOT NULL
);


ALTER TABLE public.moviegenre OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16964)
-- Name: rating; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rating (
    username character varying(120) NOT NULL,
    series_title character varying(120) NOT NULL,
    released_year integer NOT NULL,
    rating_value integer
);


ALTER TABLE public.rating OWNER TO postgres;

--
-- TOC entry 4898 (class 2606 OID 16939)
-- Name: actor actor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actor
    ADD CONSTRAINT actor_pkey PRIMARY KEY (actor_name);


--
-- TOC entry 4902 (class 2606 OID 16963)
-- Name: appuser appuser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appuser
    ADD CONSTRAINT appuser_pkey PRIMARY KEY (username);


--
-- TOC entry 4894 (class 2606 OID 16915)
-- Name: director director_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.director
    ADD CONSTRAINT director_pkey PRIMARY KEY (director_name);


--
-- TOC entry 4888 (class 2606 OID 16882)
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (genre_name);


--
-- TOC entry 4890 (class 2606 OID 16891)
-- Name: movie movie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (series_title, released_year);


--
-- TOC entry 4900 (class 2606 OID 16947)
-- Name: movieactor movieactor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movieactor
    ADD CONSTRAINT movieactor_pkey PRIMARY KEY (series_title, released_year, actor_name);


--
-- TOC entry 4896 (class 2606 OID 16923)
-- Name: moviedirector moviedirector_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.moviedirector
    ADD CONSTRAINT moviedirector_pkey PRIMARY KEY (series_title, released_year, director_name);


--
-- TOC entry 4892 (class 2606 OID 16899)
-- Name: moviegenre moviegenre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.moviegenre
    ADD CONSTRAINT moviegenre_pkey PRIMARY KEY (series_title, released_year, genre_name);


--
-- TOC entry 4904 (class 2606 OID 16971)
-- Name: rating rating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_pkey PRIMARY KEY (username, series_title, released_year);


--
-- TOC entry 4909 (class 2606 OID 16953)
-- Name: movieactor movieactor_actor_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movieactor
    ADD CONSTRAINT movieactor_actor_name_fkey FOREIGN KEY (actor_name) REFERENCES public.actor(actor_name);


--
-- TOC entry 4910 (class 2606 OID 16948)
-- Name: movieactor movieactor_series_title_released_year_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movieactor
    ADD CONSTRAINT movieactor_series_title_released_year_fkey FOREIGN KEY (series_title, released_year) REFERENCES public.movie(series_title, released_year);


--
-- TOC entry 4907 (class 2606 OID 16929)
-- Name: moviedirector moviedirector_director_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.moviedirector
    ADD CONSTRAINT moviedirector_director_name_fkey FOREIGN KEY (director_name) REFERENCES public.director(director_name);


--
-- TOC entry 4908 (class 2606 OID 16924)
-- Name: moviedirector moviedirector_series_title_released_year_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.moviedirector
    ADD CONSTRAINT moviedirector_series_title_released_year_fkey FOREIGN KEY (series_title, released_year) REFERENCES public.movie(series_title, released_year);


--
-- TOC entry 4905 (class 2606 OID 16905)
-- Name: moviegenre moviegenre_genre_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.moviegenre
    ADD CONSTRAINT moviegenre_genre_name_fkey FOREIGN KEY (genre_name) REFERENCES public.genre(genre_name);


--
-- TOC entry 4906 (class 2606 OID 16900)
-- Name: moviegenre moviegenre_series_title_released_year_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.moviegenre
    ADD CONSTRAINT moviegenre_series_title_released_year_fkey FOREIGN KEY (series_title, released_year) REFERENCES public.movie(series_title, released_year);


--
-- TOC entry 4911 (class 2606 OID 16977)
-- Name: rating rating_series_title_released_year_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_series_title_released_year_fkey FOREIGN KEY (series_title, released_year) REFERENCES public.movie(series_title, released_year);


--
-- TOC entry 4912 (class 2606 OID 16972)
-- Name: rating rating_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_username_fkey FOREIGN KEY (username) REFERENCES public.appuser(username);


-- Completed on 2025-12-02 14:48:28

--
-- PostgreSQL database dump complete
--

\unrestrict kocDwYcvUAAdFYG4VqStEudQRnkjnoPM5dyAThbVZ0kJnABpfXBTdS2vrwdycea

