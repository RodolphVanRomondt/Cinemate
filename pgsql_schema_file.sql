CREATE TABLE "roles"(
    "id" SERIAL NOT NULL,
    "actor_id" INTEGER NOT NULL,
    "movie_id" INTEGER NOT NULL
);
ALTER TABLE
    "roles" ADD PRIMARY KEY("id");
CREATE TABLE "directors"(
    "id" SERIAL NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "directors" ADD PRIMARY KEY("id");
CREATE TABLE "movies"(
    "id" SERIAL NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "rated" VARCHAR(255) NOT NULL,
    "release_year" DATE NOT NULL,
    "sutdio_id" INTEGER NOT NULL,
    "rating" DOUBLE PRECISION NOT NULL,
    "genre" VARCHAR(255) NOT NULL,
    "boxoffice" INTEGER NOT NULL
);
ALTER TABLE
    "movies" ADD PRIMARY KEY("id");
CREATE TABLE "list_movies"(
    "id" SERIAL NOT NULL,
    "list_id" INTEGER NOT NULL,
    "movie_id" INTEGER NOT NULL
);
ALTER TABLE
    "list_movies" ADD PRIMARY KEY("id");
CREATE TABLE "actors"(
    "id" SERIAL NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "actors" ADD PRIMARY KEY("id");
CREATE TABLE "lists"(
    "id" SERIAL NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "user" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "lists" ADD PRIMARY KEY("id");
ALTER TABLE
    "lists" ADD CONSTRAINT "lists_name_unique" UNIQUE("name");
CREATE TABLE "directing"(
    "id" SERIAL NOT NULL,
    "director_id" INTEGER NOT NULL,
    "movie_id" INTEGER NOT NULL
);
ALTER TABLE
    "directing" ADD PRIMARY KEY("id");
CREATE TABLE "users"(
    "username" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("username");
CREATE TABLE "studios"(
    "id" SERIAL NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "studios" ADD PRIMARY KEY("id");
ALTER TABLE
    "list_movies" ADD CONSTRAINT "list_movies_movie_id_foreign" FOREIGN KEY("movie_id") REFERENCES "movies"("id");
ALTER TABLE
    "directing" ADD CONSTRAINT "directing_movie_id_foreign" FOREIGN KEY("movie_id") REFERENCES "movies"("id");
ALTER TABLE
    "list_movies" ADD CONSTRAINT "list_movies_list_id_foreign" FOREIGN KEY("list_id") REFERENCES "lists"("id");
ALTER TABLE
    "lists" ADD CONSTRAINT "lists_user_foreign" FOREIGN KEY("user") REFERENCES "users"("username");
ALTER TABLE
    "movies" ADD CONSTRAINT "movies_sutdio_id_foreign" FOREIGN KEY("sutdio_id") REFERENCES "studios"("id");
ALTER TABLE
    "directing" ADD CONSTRAINT "directing_director_id_foreign" FOREIGN KEY("director_id") REFERENCES "directors"("id");
ALTER TABLE
    "roles" ADD CONSTRAINT "roles_movie_id_foreign" FOREIGN KEY("movie_id") REFERENCES "movies"("id");
ALTER TABLE
    "roles" ADD CONSTRAINT "roles_actor_id_foreign" FOREIGN KEY("actor_id") REFERENCES "actors"("id");