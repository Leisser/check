from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    password: str
    first_name: str
    last_name: str
    other_name: str
    address: str
    phone_number: str
    email: str
    passport_number: str
    national_identification_number: str
    date_of_birth: datetime
    country: str
    is_clerk: bool
    is_admin: bool
    is_super_admin: bool
    is_a_admin: bool
    status: int



    class Config:
        orm_mode = True




class UserLogin(BaseModel):
    password: str
    passport_number: str

    class Config:
        orm_mode = True
    

class CountryList(BaseModel):
    country_code: str
    country_name: str
    checklist: str
    status: int


    class Config:
        orm_mode = True



# class Student(BaseModel):
#     studentnunber: str
#     schoolcode: str
#     classlevel: str
#     year: str
#     term: str
#     Stream: str


#     class Config:
#         orm_mode = True

class CheckList(BaseModel):
    subject: int
    result: str
    helthfacility: str
    doctor: str

    class Config:
        orm_mode = True

class CheckPoint(BaseModel):
    user: int
    location: str
    officer: int
    post: str

    class Config:
        orm_mode = True




        