import datetime
import os
import bcrypt
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from sqlalchemy.future import select

from models import User
from models import User as ModelUser
from models import CheckList as ModelCheckList
from models import CheckPoint as ModelCheckPoint
from models import CountryList as ModelCountryList
from schema import User as SchemaUser
from schema import UserLogin as SchemaUserLogin
from schema import CheckList as SchemaCheckList
from schema import CheckPoint as SchemaCheckPoint
from schema import CountryList as SchemaCountryList



load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get("/")
async def root():
    return {"message": "😎😎 This Works fine"}

# users = []

# @app.post("/users", response_model=SchemaUser, tags=["users"])
# def create_user(user: SchemaUser):
#     users.append(user)
#     return user

# @app.get("/users/", response_model=SchemaUser, tags=["users"])
# async def get_users():
#     users = await db.session.query(ModelUser).all()
#     return users

# @app.get("/users/", response_model=SchemaUser, tags=["users"])
# async def get_users():
#     all_users = await db.session.query(ModelUser).all()
#     return [user async for user in all_users]

@app.get("/users/", tags=["users"],dependencies=[Depends(jwtBearer())])
def get_users():
    all_users = db.session.query(User).all()

    return all_users

@app.get("/user/getby/{user_id}/", tags=["users"], dependencies=[Depends(jwtBearer())])
def find_user(user_id: int):
    schoolpal_user = db.session.query(ModelUser).filter_by(user_id=user_id).first()
    if not schoolpal_user:
        raise HTTPException(status_code=404, detail="User not found")
    return schoolpal_user



@app.post("/user/register/", response_model=SchemaUser, tags=["users"])
def register_user(user: SchemaUser):
    if not user.password:
        raise HTTPException(status_code=400, detail="Password is required")
    if not user.first_name:
        raise HTTPException(status_code=400, detail="First name is required")
    if not user.last_name:
        raise HTTPException(status_code=400, detail="Last name is required")
    if not user.email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not user.country:
        raise HTTPException(status_code=400, detail="Country is required")

    if user.is_clerk and not user.is_admin:
        raise HTTPException(status_code=403, detail="User is not authorized to create a new user")
    
    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    password_hash = hashed_password.decode('utf8')

    try:
        schoolpal_user = ModelUser(
            
            password=password_hash,
            first_name=user.first_name,
            last_name=user.last_name,
            other_name=user.other_name,
            address=user.address,
            phone_number=user.phone_number,
            email=user.email,
            passport_number=user.passport_number,
            national_identification_number=user.national_identification_number,
            date_of_birth=user.date_of_birth,
            country=user.country,
            is_clerk=user.is_clerk,
            is_admin=user.is_admin,
            is_super_admin=user.is_super_admin,
            is_a_admin=user.is_a_admin,
            status= user.status
        )
        db.session.add(schoolpal_user)
        db.session.commit()
        return schoolpal_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/user/login", tags=["users"])
def user_login(user: SchemaUserLogin = Body(default=None)):
    # Find the user in the database
    schoolpal_user = db.session.query(User).filter_by(passport_number=user.passport_number).first()

    if not schoolpal_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the password is correct
    if not bcrypt.checkpw(user.password.encode("utf-8"), schoolpal_user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Incorrect password")
    

    return {
        "user_id": schoolpal_user.user_id,
        "password": schoolpal_user.password,
        "first_name": schoolpal_user.first_name,
        "last_name": schoolpal_user.last_name,
        "other_name": schoolpal_user.other_name,
        "address": schoolpal_user.address,
        "phone_number": schoolpal_user.phone_number,
        "email": schoolpal_user.email,
        "passport_number": schoolpal_user.passport_number,
        "national_identification_number": schoolpal_user.national_identification_number,
        "date_of_birth": schoolpal_user.date_of_birth,
        "country": schoolpal_user.country,
        "date_created": schoolpal_user.date_created,
        "date_modified": schoolpal_user.date_modified,
        "is_clerk": schoolpal_user.is_clerk,
        "is_admin": schoolpal_user.is_admin,
        "is_super_admin": schoolpal_user.is_super_admin,
        "is_a_admin": schoolpal_user.is_a_admin,
        "status": schoolpal_user.status,
        "token": signJWT(user.passport_number)
    }
    



    



@app.put("/user/update/{user_id}/", tags=["users"], dependencies=[Depends(jwtBearer())])
 
def update_user(user_id: int, user: SchemaUser):
    schoolpal_user = db.session.query(ModelUser).filter_by(user_id=user_id).first()
    if not schoolpal_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user attributes if values are provided
    if user.password:
        schoolpal_user.password = user.password
    if user.first_name:
        schoolpal_user.first_name = user.first_name
    if user.last_name:
        schoolpal_user.last_name = user.last_name
    if user.other_name:
        schoolpal_user.other_name = user.other_name
    if user.address:
        schoolpal_user.address = user.address
    if user.phone_number:
        schoolpal_user.phone_number = user.phone_number
    if user.email:
        schoolpal_user.email = user.email
    if user.passport_number:
        schoolpal_user.passport_number = user.passport_number
    if user.national_identification_number:
        schoolpal_user.national_identification_number = user.national_identification_number
    if user.date_of_birth:
        schoolpal_user.date_of_birth = user.date_of_birth
    if user.country:
        schoolpal_user.country = user.country
    if user.is_clerk is not None:
        schoolpal_user.is_clerk = user.is_clerk
    if user.is_admin is not None:
        schoolpal_user.is_admin = user.is_admin
    if user.is_super_admin is not None:
        schoolpal_user.is_super_admin = user.is_super_admin
    if user.is_a_admin is not None:
        schoolpal_user.is_a_admin = user.is_a_admin
    if user.status is not None:
        schoolpal_user.status = user.status


    db.session.commit()
    db.session.refresh(schoolpal_user)
    return schoolpal_user

# @app.post("/student/register/", response_model=SchemaStudent, tags=["student"])
# def register_school(student: SchemaStudent):
#     schoolpal_student = ModelStudent(studentnunber=student.studentnunber,schoolcode=student.schoolcode,classlevel=student.classlevel,year=student.year,term=student.term,Stream=student.Stream)
#     db.session.add(schoolpal_student)
#     db.session.commit()
#     return schoolpal_student;


@app.delete("/user/delete/{user_id}/", tags=["users"], dependencies=[Depends(jwtBearer())])
def delete_user(user_id: int):
    schoolpal_user = db.session.query(ModelUser).filter_by(user_id=user_id).first()
    if not schoolpal_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.session.delete(schoolpal_user)
    db.session.commit()
    return {
        "msg" : "record deleted"
    }

# @app.delete("/user/{user_id}/", tags=["users"])
# async def delete_user(user_id: int, token: str = Depends(get_jwt_token)):
#     schoolpal_user = db.session.query(ModelUser).filter_by(user_id=user_id).first()
#     if not schoolpal_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.session.delete(schoolpal_user)
#     db.session.commit()
#     return None

@app.get("/country/", tags=["countrys"],dependencies=[Depends(jwtBearer())])
def get_countrys():
    all_country = db.session.query(ModelCountryList).all()

    return all_country

@app.get("/country/{country_code}/", tags=["countrys"], dependencies=[Depends(jwtBearer())])
def find_country(country_code: str):
    country_disease = db.session.query(ModelCountryList).filter_by(country_code=country_code).first()
    if not country_disease:
        raise HTTPException(status_code=404, detail="Country not found")
    return country_disease



@app.post("/country/register/", response_model=SchemaCountryList, tags=["countrys"], dependencies=[Depends(jwtBearer())])
def register_country(country: SchemaCountryList):
    if not country.country_code:
        raise HTTPException(status_code=400, detail="Country code is required")
    if not country.country_name:
        raise HTTPException(status_code=400, detail="Country name is required")
    if not country.checklist:
        raise HTTPException(status_code=400, detail="Country disease list is required")
    

    try:
        country_disease= ModelCountryList(
            country_code=country.country_code,
            country_name=country.country_name,
            checklist=country.checklist,
            status= country.status
        )
        db.session.add(country_disease)
        db.session.commit()
        return country_disease
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





@app.put("/country/{country_code}/", tags=["countrys"], dependencies=[Depends(jwtBearer())])
 
def update_country(country_code: str, country: SchemaCountryList):
    country_disease= db.session.query(ModelCountryList).filter_by(country_code=country_code).first()
    if not country_disease:
        raise HTTPException(status_code=404, detail="Country not found")

    # Update the user attributes if values are provided
    if country.country_code:
        country_disease.country_code = country.country_code
    if country.country_name:
        country_disease.country_name = country.country_name
    if country.checklist:
        country_disease.checklist = country.checklist
    if country.status is not None:
        country_disease.status = country.status


    db.session.commit()
    db.session.refresh(country_disease)
    return country_disease

# @app.post("/student/register/", response_model=SchemaStudent, tags=["student"])
# def register_school(student: SchemaStudent):
#     schoolpal_student = ModelStudent(studentnunber=student.studentnunber,schoolcode=student.schoolcode,classlevel=student.classlevel,year=student.year,term=student.term,Stream=student.Stream)
#     db.session.add(schoolpal_student)
#     db.session.commit()
#     return schoolpal_student;


@app.delete("/country/{country_code}/", tags=["countrys"], dependencies=[Depends(jwtBearer())])
def delete_country(country_code: str):
    country_disease = db.session.query(ModelCountryList).filter_by(country_code=country_code).first()
    if not country_disease:
        raise HTTPException(status_code=404, detail="User not found")
    db.session.delete(country_disease)
    db.session.commit()
    return {
        "msg" : "record deleted"
    }

#CheckList

@app.get("/results/", tags=["results"],dependencies=[Depends(jwtBearer())])
def get_results():
    all_results = db.session.query(ModelCheckList).all()

    return all_results

@app.get("/results/{checklist_id}/", tags=["results"], dependencies=[Depends(jwtBearer())])
def find_results(checklist_id: int):
    checked_disease = db.session.query(ModelCheckList).filter_by(checklist_id=checklist_id).first()
    if not checked_disease:
        raise HTTPException(status_code=404, detail="Result not found")
    return checked_disease



@app.post("/results/register/", response_model=SchemaCheckList, tags=["results"], dependencies=[Depends(jwtBearer())])
def register_results(results: SchemaCheckList):
    if not results.subject:
        raise HTTPException(status_code=400, detail="Subject is required")
    if not results.result:
        raise HTTPException(status_code=400, detail="Result is required")
    if not results.helthfacility:
        raise HTTPException(status_code=400, detail="Helth Facility is required")
    if not results.doctor:
        raise HTTPException(status_code=400, detail="Doctor is required")
    

    try:
        checked_disease= ModelCheckList(
            subject=results.subject,
            result=results.result,
            helthfacility= results.helthfacility,
            doctor= results.doctor
        )
        db.session.add(checked_disease)
        db.session.commit()
        return checked_disease
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





@app.put("/results/{checklist_id}/", tags=["results"], dependencies=[Depends(jwtBearer())])
 
def update_results(checklist_id: int, results: SchemaCheckList):
    checked_disease= db.session.query(ModelCheckList).filter_by(checklist_id=checklist_id).first()
    if not checked_disease:
        raise HTTPException(status_code=404, detail="Result not found")

    # Update the user attributes if values are provided
    if results.subject:
        checked_disease.subject = results.subject
    if results.result:
        checked_disease.result = results.result
    if results.helthfacility:
        checked_disease.helthfacility = results.helthfacility
    if results.doctor:
        checked_disease.doctor = results.doctor


    db.session.commit()
    db.session.refresh(checked_disease)
    return checked_disease

# @app.post("/student/register/", response_model=SchemaStudent, tags=["student"])
# def register_school(student: SchemaStudent):
#     schoolpal_student = ModelStudent(studentnunber=student.studentnunber,schoolcode=student.schoolcode,classlevel=student.classlevel,year=student.year,term=student.term,Stream=student.Stream)
#     db.session.add(schoolpal_student)
#     db.session.commit()
#     return schoolpal_student;


@app.delete("/results/{checklist_id}/", tags=["results"], dependencies=[Depends(jwtBearer())])
def delete_results(checklist_id: int):
    checked_disease = db.session.query(ModelCheckList).filter_by(checklist_id=checklist_id).first()
    if not checked_disease:
        raise HTTPException(status_code=404, detail="Result not found")
    db.session.delete(checked_disease)
    db.session.commit()
    return {
        "msg" : "record deleted"
    }

# CheckPoint

@app.get("/checkpoint/", tags=["checkpoints"],dependencies=[Depends(jwtBearer())])
def get_checkpoints():
    all_points = db.session.query(ModelCheckPoint).all()

    return all_points

@app.get("/checkpoint/{checkpoint_id}/", tags=["checkpoints"], dependencies=[Depends(jwtBearer())])
def find_checkpoints(checkpoint_id: int):
    check_point = db.session.query(ModelCheckPoint).filter_by(checkpoint_id=checkpoint_id).first()
    if not check_point:
        raise HTTPException(status_code=404, detail="Point not found")
    return check_point

@app.get("/checkpoint/{user}/", tags=["checkpoints"], dependencies=[Depends(jwtBearer())])
def find_checkpoints(user: int):
    check_points = db.session.query(ModelCheckList).filter_by(user=user).all()
    if not check_points:
        raise HTTPException(status_code=404, detail="Points not found")
    return check_points

@app.get("/checkpoint/{officer}/", tags=["checkpoints"], dependencies=[Depends(jwtBearer())])
def find_checkpoints(officer: int):
    check_points = db.session.query(ModelCheckList).filter_by(officer=officer).all()
    if not check_points:
        raise HTTPException(status_code=404, detail="Checkpoints not found")
    return check_points



@app.post("/checkpoint/register/", response_model=SchemaCheckPoint, tags=["checkpoints"], dependencies=[Depends(jwtBearer())])
def register_checkpoints(checkpoint: SchemaCheckPoint):
    if not checkpoint.user:
        raise HTTPException(status_code=400, detail="User is required")
    if not checkpoint.location:
        raise HTTPException(status_code=400, detail="Location is required")
    if not checkpoint.officer:
        raise HTTPException(status_code=400, detail="Officer is required")
    if not checkpoint.post:
        raise HTTPException(status_code=400, detail="post is required")
    

    try:
        check_point= ModelCheckPoint(
            user=checkpoint.user,
            location=checkpoint.location,
            officer= checkpoint.officer,
            post= checkpoint.post
        )
        db.session.add(check_point)
        db.session.commit()
        return check_point
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





@app.put("/checkpoint/{checkpoint_id}/", tags=["checkpoints"], dependencies=[Depends(jwtBearer())])
 
def update_checkpoints(checkpoint_id: int, checkepoint: SchemaCheckPoint):
    checked_point= db.session.query(ModelCheckPoint).filter_by(checkpoint_id=checkpoint_id).first()
    if not checked_point:
        raise HTTPException(status_code=404, detail="Checkpoint not found")

    # Update the user attributes if values are provided
    if checkepoint.user:
        checked_point.user = checkepoint.user
    if checkepoint.location:
        checked_point.location = checkepoint.location
    if checkepoint.officer:
        checked_point.officer = checkepoint.officer
    if checkepoint.post:
        checked_point.post = checkepoint.post


    db.session.commit()
    db.session.refresh(checked_point)
    return checked_point

# @app.post("/student/register/", response_model=SchemaStudent, tags=["student"])
# def register_school(student: SchemaStudent):
#     schoolpal_student = ModelStudent(studentnunber=student.studentnunber,schoolcode=student.schoolcode,classlevel=student.classlevel,year=student.year,term=student.term,Stream=student.Stream)
#     db.session.add(schoolpal_student)
#     db.session.commit()
#     return schoolpal_student;


@app.delete("/checkpoint/{checkpoint_id}/", tags=["checkpoints"], dependencies=[Depends(jwtBearer())])
def delete_checkpoints(checkpoint_id: int):
    checked_disease = db.session.query(ModelCheckPoint).filter_by(checkpoint_id=checkpoint_id).first()
    if not checked_disease:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    db.session.delete(checked_disease)
    db.session.commit()
    return {
        "msg" : "record deleted"
    }


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)