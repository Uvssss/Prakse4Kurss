create table battery_info(
    id int not null,
    startime varchar(100) not null,
    endtime varchar(100) not null,
    KW float not null,
    `capacity` float not null, 
    price float not null,
    `status` tinyint(1) not null,
    foreign key(id) references electricity(id)
);