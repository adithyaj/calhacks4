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
