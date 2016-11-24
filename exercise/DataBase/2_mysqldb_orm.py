#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


"""Average score from people whose age is over 30"""
"""
SELECT avg(sc.score) FROM scores sc
JOIN students st ON sc.studentID = st.stID
WHERE st.Age >= 30;
"""


from mysqldb_orm_model import Student, Score
from exer_connection_db import mysql_account, server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

connection_string = "mysql+mysqldb://{}:{}@{}:3306/test2"\
                    .format(mysql_account['id'], mysql_account['pw'], server)

engine = create_engine(connection_string, pool_recycle = 3600, encoding = 'utf-8')
Session = sessionmaker(bind=engine)
session = Session()

result = session.query(func.avg(Score.Score))\
                .join(Student, Student.stID == Score.StudentID)\
                .filter(Student.Age >= 30)\
                .all()

for row in result:
    print row


"""Course attendant whose age is under 27"""
"""
SELECT sc.CourseCode FROM scores sc
JOIN students st ON sc.studentID = st.stID
WHERE st.Age <= 27;
"""

result = session.query(Score.CourseCode)\
                .join(Student, Student.stID == Score.StudentID)\
                .filter(Student.Age <= 27)

for row in result:
    print row


"""Avgerage score per course"""
"""
SELECT CourseCode, avg(Score) FROM scores
GROUP BY CourseCode;
"""

result = session.query(Score.CourseCode, func.avg(Score.Score))\
                .group_by(Score.CourseCode)\
                .all()

for row in result:
    print row                
