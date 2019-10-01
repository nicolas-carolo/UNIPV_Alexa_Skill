from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Professor(Base):
	__tablename__ = 'professors'

	email = Column(String, primary_key=True)
	full_name =Column(String)
	surname = Column(String)
	name = Column(String)
	gender = Column(String)
	office = Column(String)
	lab = Column(String)
	office_hour = Column(String)


class Course(Base):
	__tablename__ = 'courses'

	course_name = Column(String, primary_key=True)
	alias = Column(String)
	professor = Column(String, primary_key=True)
    
class Exam(Base):
	
	__tablename__ = 'exams'
	
	id = Column(Integer, primary_key=True)
	course_name = Column(String)
	short = Column(String)
	date = Column(Date)
	room = Column(Integer)
	time = Column(Integer)
	
class Schedule(Base):
	
	__tablename__ = 'schedule'
	
	id = Column(Integer, primary_key=True)
	day = Column(Integer)
	course = Column(String)
	alias = Column(String)
	time = Column(Integer)
	room = Column(String)
	year = Column(Integer)
	
class Menu(Base):
	
	__tablename__ = 'menu'
	
	day = Column(Integer, primary_key=True)
	first = Column(String)
	second = Column(String)
	side = Column(Integer)
	
class User(Base):

	__tablename__ = 'users'
	
	name = Column(String, primary_key=True)
	year = Column(Integer)
	active = Column(Boolean)
	
class Calendar(Base):
	
	__tablename__ = 'calendar'
	
	activity = Column(String)
	start = Column(Date, primary_key=True)
	end = Column(Date)
