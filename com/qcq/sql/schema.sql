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