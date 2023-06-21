set autocommit = 0;
create database customers_db;
use customers_db;
create table customers_table(
	customer_id int PRIMARY KEY auto_increment,
    	customer_name varchar(16) not null,
    	customer_cash int default 0,
	customer_password varchar(20) default "password"
);
insert into customers_table(customer_name, customer_cash) value
	("mark robert", 1000000),
    ("zack chi", 205500),
    ("admin", 999999);

update customers_table
set customer_password = concat("password", customer_id);
select * from customers_table;
commit;
