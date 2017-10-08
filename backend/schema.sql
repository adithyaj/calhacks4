create table if not exists users (
    id integer primary key autoincrement,
    username text not null,
    hashword text not null
);

create table if not exists result_locations (
    id integer primary key autoincrement,
    place text not null,
    class integer default 0
);