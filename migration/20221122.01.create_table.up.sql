CREATE TABLE locations
(
    id   SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(30)        NOT NULL,
    slug VARCHAR(30)        NOT NULL
);

ALTER TABLE locations
    ADD CONSTRAINT fk1_unique UNIQUE (name);







