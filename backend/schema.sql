create table if not exists users (
    id integer primary key autoincrement,
    username text not null,
    hashword text not null
);
drop table if exists results;
create table if not exists results (
    id integer primary key autoincrement,
    place text not null,
    latitude real default 0.0,
    longitude real default 0.0,
    hits integer default 0
);
drop table if exists tags;
create table if not exists tags (
    id integer primary key autoincrement,
    tag text UNIQUE
);
drop table if exists result_tag;
create table if not exists result_tag (
    r_id integer REFERENCES results(id),
    t_id integer REFERENCES tags(id)
);
