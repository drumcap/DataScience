#courses 테이블과 scores 테이블로 작업
use test2;
DROP TABLE courses;

CREATE TABLE courses (
ID INT(11) NOT NULL AUTO_INCREMENT,
Code VARCHAR(20) NOT NULL DEFAULT '',
Name VARCHAR(20) NOT NULL DEFAULT '',
PRIMARY KEY (ID)
)
DEFAULT CHARSET = utf8;

CREATE TABLE scores (
ID INT(11) NOT NULL AUTO_INCREMENT,
StudentID VARCHAR(20) NOT NULL DEFAULT "",
CourseCode VARCHAR(20) NOT NULL DEFAULT "",
Score FLOAT(11) NOT NULL DEFAULT 0,
PRIMARY KEY (ID)
)
DEFAULT CHARSET = utf8;

SELECT * FROM courses;
SELECT * FROM scores;

INSERT INTO courses VALUES(1, 'CS', 'Computer Science');
INSERT INTO courses VALUES(2, 'ME', 'Mechanical engineering');
INSERT INTO courses VALUES(3, 'EE', 'Electrical engineering');
INSERT INTO courses VALUES(4, 'BIO', 'Biology');

INSERT INTO scores VALUES(1, 'A123', 'CS', 45);
INSERT INTO scores VALUES(2, 'A123', 'EE', 55);
INSERT INTO scores VALUES(3, 'A126', 'CS', 80);
INSERT INTO scores VALUES(4, 'A121', 'BIO', 60);
INSERT INTO scores VALUES(5, 'A126', 'ME', 70);
INSERT INTO scores VALUES(6, 'A123', 'ME', 90);
INSERT INTO scores VALUES(7, 'A121', 'CS', 57);
INSERT INTO scores VALUES(8, 'A121', 'EE', 77);

SELECT * FROM scores;

#학생별 평균 점수
SELECT st.Name, avg(sc.Score) FROM scores sc JOIN students st ON sc.StudentID=st.stID GROUP BY StudentID;

#전공별 평균 점수
SELECT co.Name, avg(sc.Score) FROM scores sc JOIN courses co on sc.CourseCode=co.Code GROUP BY CourseCode;

#가장 많은 코스를 들은 학생과 가장 적은 코스를 들은 학생
SELECT st.name, count(*) as cnt FROM scores sc JOIN students st ON sc.StudentID=st.stID GROUP BY StudentID ORDER BY cnt DESC LIMIT 1;
SELECT st.name, count(*) FROM scores sc JOIN students st ON sc.StudentID=st.stID GROUP BY StudentID ORDER BY count(*) LIMIT 1;

#전체 평균보다 낮은 점수를 기록한 학생
SELECT st.name, avg(sc.score) FROM scores sc JOIN students st ON sc.StudentID=st.stID GROUP BY StudentID HAVING avg(score) < (SELECT avg(score) FROM scores);





SELECT * FROM students;
UPDATE students SET stID='A126' WHERE NAME='Aaron';
UPDATE students SET stID='A123' WHERE NAME='Bob';
UPDATE students SET stID='A121' WHERE NAME='Alice';
UPDATE students SET stID='A127' WHERE NAME='Amy';

DELETE FROM students WHERE MajorCode is NULL;
SELECT * FROM students;
SELECT * FROM scores;



#world database
#GNP가 가장 높은 나라는?
SELECT Name, GNP FROM country order by GNP DESC limit 1;
#각 나라의 주요 도시별 평균 인구수는?
SELECT co.Name, avg(ct.Population) FROM city ct JOIN country co ON ct.CountryCode = co.Code GROUP BY CountryCode;
#기대수명이 평균보다 낮은 나라들의 평균 GNP는?
SELECT Name, GNP FROM country WHERE LifeExpectancy <= (SELECT avg(LifeExpectancy) FROM country);
SELECT avg(GNP) FROM country WHERE LifeExpectancy <= (SELECT avg(LifeExpectancy) FROM country);
#각 나라에서 가장 많이 쓰는 언어와 비율
SELECT co.Name, cl.Language, max(cl.Percentage) FROM countrylanguage cl JOIN country co ON co.Code = cl.CountryCode GROUP BY co.Name;
