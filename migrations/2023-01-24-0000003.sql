create table electricity_connection(
	`startime` varchar(100)  not null,
    `endtime` varchar(100)  not null,
    `savedEUR` float not null,
    electricty_id int not null,
	foreign key(electricty_id) references Electricity(id)
);