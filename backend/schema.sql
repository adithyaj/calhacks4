create table if not exists users (
    id integer primary key autoincrement,
    username text not null,
    hashword text not null
);