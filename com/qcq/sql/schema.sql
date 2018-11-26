CREATE TABLE todo (
    id INT AUTO_INCREMENT,
    title TEXT,
    primary key (id)
);


create table pictures(
	id serial primary key,
	name text,
	path text,
	media_id text,
	created_at text,
	created timestamp default now()
);