set autocommit = 0;
create database customers_db;
use customers_db;
create table customers_table(
	customer_id int unique,
    customer_name varchar(16) not null,
    customer_cash int default 0
);
insert into customers_table value
	(1, "Mark Robert", 1000000),
    (2, "Zack Chi", 205500),
    (3, "admin", 999999);
select * from customers_table;
commit;
alter table customers_table
add column password varchar(16) default "password";
commit;
