create database ebook;
\c ebook;
CREATE TABLE todo (
    id serial primary key,
    title TEXT,
    created timestamp default now()
);

#create table used for store the pictures.
create table pictures(
	id serial primary key,
	name text,
	path text,
	media_id text,
	created_at text,
	created timestamp default now()
);


# create table used for blogs.
CREATE TABLE entries (
    id serial primary key,
    title TEXT,
    content TEXT,
    posted_on timestamp default now()
);

# create the sessions
create table sessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);

# users
CREATE TABLE users
(
  id serial NOT NULL,
  name character varying(80) NOT NULL,
  pass character(40) NOT NULL,
  email character varying(100) NOT NULL,
  privilege integer NOT NULL DEFAULT 0,
  CONSTRAINT utilisateur_pkey PRIMARY KEY (id)
);