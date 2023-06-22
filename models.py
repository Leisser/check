from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()




class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    other_name = Column(String(255))
    address = Column(String(255))
    phone_number = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    passport_number = Column(String(255))
    national_identification_number = Column(String(255))
    date_of_birth = Column(DateTime(timezone=False))
    country = Column(String(255))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now())
    is_clerk = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_super_admin = Column(Boolean, default=False)
    is_a_admin = Column(Boolean, default=False)
    status = Column(Integer)
    


class CountryList(Base):
    __tablename__ = "countrylist"
    country_code = Column(String(3), primary_key=True)
    country_name = Column(String(100))
    checklist = Column(String)
    status = Column(Integer)



# class Student(Base):
#     __tablename__ = "student"
#     id = Column(Integer, index=True)
#     studentnunber = Column(String, ForeignKey("user.usercode"), primary_key=True)
#     schoolcode = Column(String, ForeignKey("school.Schoolcode"))
#     classlevel = Column(String)
#     year = Column(String)
#     term = Column(String)
#     Stream = Column(String)

#     school = relationship("School")
#     user = relationship("User")


class CheckList(Base):
    __tablename__ = "checklist"
    checklist_id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    result = Column(String(100))
    dateofoccurence = Column(DateTime(timezone=True), server_default=func.now())
    helthfacility = Column(String(100))
    doctor = Column(String(100))

    user = relationship("User")

class CheckPoint(Base):
    __tablename__ = "checkpoint"
    checkpoint_id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    location = Column(String(100))
    dateofoccurence = Column(DateTime(timezone=True), server_default=func.now())
    officer = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    post = Column(String(100))

    user = relationship("User")

    