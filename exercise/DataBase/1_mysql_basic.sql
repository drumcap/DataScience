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

INSERT INTO students values(1, "Aaron", 31, 'CS');
INSERT INTO students values(2, "Bob", 30, 'BIO');
INSERT INTO students values(3, "Alice", 24, 'PHIL');

INSERT INTO students(Name, MajorCode) values("홍길동", 'CHE');
INSERT INTO students values(5, "홍길똥", 32, 'EE');
INSERT INTO students(Name, Age, majorCode) values("Amy", 27, 'CS');
INSERT INTO students(Name, Age, majorCode) values("Jason", 22, 'CS');
INSERT INTO students(Name, Age, MajorCode) values("Bill", 20, 'EE');
INSERT INTO students(MajorCode) values('EE');
UPDATE students set Name = 'Tim' where Name = '';
DELETE FROM students where Name = 'Tim';

CREATE INDEX students_name_idx ON students(Name);
SELECT * FROM students WHERE Name = 'Aaron';
SELECT * FROM students WHERE Name != 'Aaron';
SELECT * FROM students WHERE Name <> 'Aaron';
SELECT * FROM students WHERE Name = 'Aaron' and MajorCode = 'CS';
CREATE INDEX students_name_major_idx ON students(Name, MajorCode);
SELECT * FROM students WHERE Name = 'Aaron' and MajorCode = 'CS';
SELECT * FROM students ORDER BY MajorCode DESC;
SELECT * FROM students ORDER BY MajorCode, Name DESC;
SELECT count(*) FROM students;
SELECT count(*) FROM students WHERE MajorCode='CS';
SELECT sum(Age) FROM students;
SELECT avg(Age) FROM students;
SELECT sum(Age) /2 FROM students;
SELECT Age, Age/2 FROM students;
SELECT * FROM students WHERE Age BETWEEN 20 AND 30;
SELECT * FROM students WHERE Name is NULL;
SELECT * FROM students WHERE Name is not NULL;
SELECT DISTINCT MajorCode FROM students;
SELECT max(Age), min(Age) FROM students;
SELECT * FROM students GROUP BY MajorCode;
SELECT MajorCode, sum(Age), avg(Age), max(Age), min(Age) FROM students GROUP BY MajorCode;
SELECT sum(Age), avg(Age), max(Age), min(Age) FROM students GROUP BY MajorCode;
#SELECT MajorCode, max(Age), min(Age), avg(Age) FROM students GROUP BY MajorCode WHERE avg(Age) <= 27;
SELECT MajorCode, max(Age), min(Age), avg(Age) FROM students WHERE avg(Age) <= 27 GROUP BY MajorCode;
SELECT majorCode, max(Age), min(Age), avg(Age) FROM students WHERE MajorCode = 'CS' GROUP BY MajorCode;
#SELECT majorCode, max(Age), min(Age), avg(Age) FROM students GROUP BY MajorCode WHERE MajorCode = 'CS';
SELECT MajorCode, max(Age), min(Age), avg(Age) FROM students GROUP BY MajorCode HAVING MajorCode = 'CS';
SELECT MajorCode, max(Age), min(Age), avg(Age) FROM students GROUP BY MajorCode HAVING avg(Age) <= 27;
#SELECT MajorCode, max(Age), min(Age), avg(Age) FROM students HAVING avg(Age) <=27;
SELECT MajorCode, max(Age), min(Age), avg(Age) FROM students;
SELECT MajorCode, max(Age), min(Age), avg(Age) FROM students WHERE Age <= 27;
#SELECT MajorCode, max(Age), min(Age), avg(Age) FROM students WHERE avg(Age) <= 27;
SELECT MajorCode, max(Age), min(Age), avg(Age) FROM students WHERE Age <= 27 GROUP BY MajorCode;
SELECT MajorCode, max(Age), min(Age), avg(Age) FROM students GROUP BY MajorCode;
SELECT * FROM students WHERE Age > (SELECT avg(age) FROM students);
SELECT min(Age) FROM (SELECT * FROM students WHERE Age > 26) as t;
SELECT min(Age) FROM (SELECT Age FROM students WHERE Age > 26) as t;

INSERT INTO majors(Code, Name, Description) VALUES('CS', 'Computer Science', 'CSCSCSCS');
INSERT INTO majors(Code, Name, Description) VALUES('BIO', 'Biology', 'Bioloy hahaha');
INSERT INTO majors(Code, Name, Description) VALUES('PHIL', 'Philosophy', 'Good');
INSERT INTO majors(Code, Name, Description) VALUES('CHE', 'Chemistry', 'Better');
INSERT INTO majors(Code, Name, Description) VALUES('EE', 'Electrical Engineering', 'Best');
INSERT INTO majors(Code, Name, Description) VALUES('ECO', 'Economics', 'Even Better');

SELECT * FROM students;
SELECT * FROM majors;
SELECT * FROM students CROSS JOIN majors;
SELECT * FROM students, majors;
SELECT * FROM students AS s INNER JOIN majors AS m ON s.MajorCode = m.Code;
SELECT * FROM students s JOIN majors m ON s.majorCode = m.Code;
SELECT * FROM students s LEFT OUTER JOIN majors m ON s.MajorCode = m.Code;
SELECT * FROM students s LEFT JOIN majors m ON s.MajorCode = m.Code;
SELECT * FROM students s RIGHT JOIN majors m ON s.MajorCode = m.Code;
#SELECT * FROM students s FULL OUTER JOIN majors m ON s.MajorCode = m.Code;
SELECT * FROM students s RIGHT JOIN majors m ON s.MajorCode = m.Code UNION SELECT * FROM students s LEFT JOIN majors m ON s.MajorCode = m.Code;
