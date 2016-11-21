use world;
show tables;
select * from country;
describe country;
select name from country;
select Code as c, Name as N from country;
select * from country
where Name='Andorra';
select * from country where Continent='Asia' and Continent='Europe';
select * from country limit 1;
insert into country values('XYZ', 'Pluto','Asia','Southern and Central Asia',796095.00,1947,156483000,61.1,61289.00,58549.00,'Pakistan','Republic','Mohammad Rafiq Tarar',2831,'PK');
select * from country where Code='XYZ';
update country set Code='YYZ', Continent = 'Asia' where Code='XYZ';
delete from country where Code='YYZ';
select * from country where Code like '%KOR%';
select * from country as co join city as ct on co.Code = ct.CountryCode where co.Code='KOR';
select co.Code, ct.* from country as co join city as ct on co.Code = ct.CountryCode where co.Code='KOR';
select sum(ct.population) from country as co join city as ct on co.Code = ct.CountryCode where co.Code='KOR';
select ct.population from country as co join city as ct on co.Code = ct.CountryCode where co.Code='KOR';

DROP SCHEMA IF EXISTS test2;
CREATE SCHEMA test2;
USE test2;

CREATE TABLE students (
ID INT(11) NOT NULL AUTO_INCREMENT,
Name CHAR(35) NOT NULL DEFAULT '',
Age INT(11) NOT NULL DEFAULT 25,
MajorCode VARCHAR(10),
PRIMARY KEY (ID)
) DEFAULT CHARSET=utf8;

SELECT * FROM students;