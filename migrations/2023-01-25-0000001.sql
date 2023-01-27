create table battery_info(
	startime varchar(100)  not null,
    endtime varchar(100)  not null,
    charge_amount float not null,
    charge_power float not null,
    electricty_id int not null,
	foreign key(electricty_id) references Electricity(id)
)