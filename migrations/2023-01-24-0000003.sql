create table electricity_connection(
	`startime` datetime not null,
    `endtime` datetime not null,
    `savedEUR` double not null,
    electricty_id int not null,
	foreign key(electricty_id) references Electricity(id)
);