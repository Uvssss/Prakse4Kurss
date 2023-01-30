create table consumption(
	`id` int not null unique auto_increment,
    `startime` varchar(45) not null,
    `endtime` varchar(45) not null,
    `items_id` int not null,
    foreign key(items_id) references items(id)
    
);