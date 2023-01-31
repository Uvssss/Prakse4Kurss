create table battery_info(
    `id` int not null auto_increment primary key,
    `name` varchar(45) not null
    `max_capacity` float not null,
    `current_capacity` float not null,
    `charge_power` float not null,
);