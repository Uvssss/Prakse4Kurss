create table prices(
	`startime` datetime not null,
    `endtime` datetime not null,
    electricty_id int not null,
	foreign key(electricty_id) references Electricity(id),
    `price` double not null
);