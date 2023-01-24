create table electricity_connection(
	`startime` datetime not null,
    `endtime` datetime not null,
    `pricekWH` varchar(45) not null,
    electricty_id int not null,
	foreign key(electricty_id) references Electricity(id)
);