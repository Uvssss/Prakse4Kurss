create table battery(
    id int not null,
    `max_capacity` float not null,
    `current_capacity` float not null,
    `charge_power` float not null,
    foreign key(id) references electricity(id)
);