create table prices(
	`startime` varchar(100)  not null,
    `endtime` varchar(100) not null,
    electricty_id int not null,
	foreign key(electricty_id) references Electricity(id),
    `price` float not null
);