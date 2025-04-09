from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Appointment(BaseModel):
    id: str
    name: str
    doctor: str
    time: str

class AppointmentCreate(BaseModel):
    name: str
    doctor: str
    time: str

appointments: List[Appointment] = []

@app.get("/appointments", response_model=List[Appointment])
def get_appointments():
    return appointments

@app.post("/appointments", response_model=Appointment)
def create_appointment(appt: AppointmentCreate):
    new_appt = Appointment(id=str(uuid4()), **appt.dict())
    appointments.append(new_appt)
    return new_appt

@app.delete("/appointments/{appt_id}")
def delete_appointment(appt_id: str):
    global appointments
    appointments = [a for a in appointments if a.id != appt_id]
    return {"message": "Deleted"}
