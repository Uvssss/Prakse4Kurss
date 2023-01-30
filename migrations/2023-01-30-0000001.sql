create table electricity_item_used(
    startime varchar(45) not null,
    electricity_used_item_id int not null,
    amount float not null,
	foreign key(electricity_used_item_id) references electricity_used_item(id)
);