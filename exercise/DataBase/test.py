from mysqldb_orm_model import Student
from exer_connection_db import mysql_account, server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

connection_string = 'mysql+mysqldb://{}:{}@{}:3306/test2'.format(mysql_account['id'], mysql_account['pw'], server)
print connection_string
engine = create_engine(connection_string, pool_recycle = 3600, encoding='utf-8')
Session = sessionmaker(bind=engine)

session = Session()

result = session.query(Student).filter(Student.Age < 30).all()

for row in result:
    print row.Age
