create table battery_info(
    id int not null auto_increment,
	startime varchar(100)  not null,
    endtime varchar(100)  not null,
    max_capacity float not null,
    current_capacity float not null,
    charge_power float not null,
    `name` varchar(45) not null
);