create table consumption(
	`id` int not null unique auto_increment,
    `starttime` varchar(45) not nullid
    `endtime` varchar(45) not null
    `items_id` int not null,
    foreign_key(items_id) references items(id)
    
);