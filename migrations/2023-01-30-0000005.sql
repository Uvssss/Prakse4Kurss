create table connection(
    startime varchar(100) not null,
    endtime varchar(100) not null,
    best_price float not null,
    used float not null,
    connection int not null,
    foreign key(connection) references electricity(id)
);