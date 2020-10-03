-- create user
create user 'myuser'@'localhost' identified by "password";
GRANT ALL ON *.* TO 'myuser'@'localhost';

-- create database
create database if not exists mydb;
use mydb;

-- test table
create table if not exists test (
    id int(11) auto_increment not null,
    name varchar(64) not null,
    primary key (id)
);
