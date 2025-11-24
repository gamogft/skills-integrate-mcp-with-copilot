"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from typing import Optional, List

from sqlmodel import SQLModel, Field, create_engine, Session, select


DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./data.db")

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


# --- SQLModel models ---
class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    schedule: str
    max_participants: int


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: Optional[str] = None
    grade: Optional[str] = None


class Enrollment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    activity_id: int = Field(foreign_key="activity.id")
    student_id: int = Field(foreign_key="student.id")


# Create engine and session helper
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


@app.on_event("startup")
def on_startup():
    # Create tables
    SQLModel.metadata.create_all(engine)

    # Seed initial activities if none exist
    with Session(engine) as session:
        count = session.exec(select(Activity)).first()
        if not count:
            seed_activities = [
                Activity(name="Chess Club", description="Learn strategies and compete in chess tournaments", schedule="Fridays, 3:30 PM - 5:00 PM", max_participants=12),
                Activity(name="Programming Class", description="Learn programming fundamentals and build software projects", schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM", max_participants=20),
                Activity(name="Gym Class", description="Physical education and sports activities", schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM", max_participants=30),
                Activity(name="Soccer Team", description="Join the school soccer team and compete in matches", schedule="Tuesdays and Thursdays, 4:00 PM - 5:30 PM", max_participants=22),
                Activity(name="Basketball Team", description="Practice and play basketball with the school team", schedule="Wednesdays and Fridays, 3:30 PM - 5:00 PM", max_participants=15),
                Activity(name="Art Club", description="Explore your creativity through painting and drawing", schedule="Thursdays, 3:30 PM - 5:00 PM", max_participants=15),
                Activity(name="Drama Club", description="Act, direct, and produce plays and performances", schedule="Mondays and Wednesdays, 4:00 PM - 5:30 PM", max_participants=20),
                Activity(name="Math Club", description="Solve challenging problems and participate in math competitions", schedule="Tuesdays, 3:30 PM - 4:30 PM", max_participants=10),
                Activity(name="Debate Team", description="Develop public speaking and argumentation skills", schedule="Fridays, 4:00 PM - 5:30 PM", max_participants=12),
            ]
            session.add_all(seed_activities)
            session.commit()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


def activity_to_dict(activity: Activity, session: Session) -> dict:
    # Gather participants for activity
    enrollments = session.exec(select(Enrollment).where(Enrollment.activity_id == activity.id)).all()
    participants: List[str] = []
    for e in enrollments:
        student = session.get(Student, e.student_id)
        if student:
            participants.append(student.email)

    return {
        "description": activity.description,
        "schedule": activity.schedule,
        "max_participants": activity.max_participants,
        "participants": participants,
    }


@app.get("/activities")
def get_activities():
    with Session(engine) as session:
        activities = session.exec(select(Activity)).all()
        result = {a.name: activity_to_dict(a, session) for a in activities}
        return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity (DB-backed)"""
    with Session(engine) as session:
        activity = session.exec(select(Activity).where(Activity.name == activity_name)).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Find or create student
        student = session.exec(select(Student).where(Student.email == email)).first()
        if not student:
            student = Student(email=email)
            session.add(student)
            session.commit()
            session.refresh(student)

        # Check if already enrolled
        exists = session.exec(select(Enrollment).where(Enrollment.activity_id == activity.id, Enrollment.student_id == student.id)).first()
        if exists:
            raise HTTPException(status_code=400, detail="Student is already signed up")

        # Check capacity
        current_count = session.exec(select(Enrollment).where(Enrollment.activity_id == activity.id)).count()
        if current_count >= activity.max_participants:
            raise HTTPException(status_code=400, detail="Activity is full")

        enrollment = Enrollment(activity_id=activity.id, student_id=student.id)
        session.add(enrollment)
        session.commit()
        return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity (DB-backed)"""
    with Session(engine) as session:
        activity = session.exec(select(Activity).where(Activity.name == activity_name)).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        student = session.exec(select(Student).where(Student.email == email)).first()
        if not student:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        enrollment = session.exec(select(Enrollment).where(Enrollment.activity_id == activity.id, Enrollment.student_id == student.id)).first()
        if not enrollment:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        session.delete(enrollment)
        session.commit()
        return {"message": f"Unregistered {email} from {activity_name}"}
