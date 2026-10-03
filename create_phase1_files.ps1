# CampusPilot Phase 1 - Backend Files Creator
# Run in VS Code Terminal (PowerShell) from project root

$root = "CampusPilot"
$b = "$root\backend\backend"

Write-Host "Creating Phase 1 backend files..." -ForegroundColor Green

# ===== requirements.txt =====
@"
fastapi==0.110.1
uvicorn[standard]==0.29.0
sqlmodel==0.0.14
python-dotenv==1.0.1
pdfplumber==0.11.4
reportlab==4.1.0
pandas==2.2.3
pydantic==2.7.1
pydantic-settings==2.3.2
pytest==8.2.0
httpx==0.27.0
"@ | Set-Content -Path "$root\requirements.txt" -Encoding UTF8
Write-Host "Created: $root\requirements.txt"

# ===== .env.example =====
@"
# CampusPilot / ClassPilot — Environment Variables
# Copy to backend/backend/.env and adjust if needed

# Database
DATABASE_URL=sqlite:///../../database/classpilot.db

# Timezone for all server-side datetime operations
TIMEZONE=Asia/Kolkata

# College hours (24h format)
COLLEGE_START=09:00
COLLEGE_END=17:00

# Lunch break (excluded from vacant-room logic)
LUNCH_START=13:00
LUNCH_END=14:00

# Attendance thresholds (percentage)
ATTENDANCE_SAFE=75
ATTENDANCE_WARNING=65

# File upload limits
MAX_UPLOAD_MB=10
ALLOWED_EXTENSIONS=.pdf,.csv
"@ | Set-Content -Path "$root\.env.example" -Encoding UTF8
Write-Host "Created: $root\.env.example"

# ===== config.py =====
@"
\"\"\"Configuration constants loaded from environment with sensible defaults.\"\"\"
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(default=\"sqlite:///../../database/classpilot.db\", alias=\"DATABASE_URL\")
    timezone: str = Field(default=\"Asia/Kolkata\", alias=\"TIMEZONE\")
    college_start: str = Field(default=\"09:00\", alias=\"COLLEGE_START\")
    college_end: str = Field(default=\"17:00\", alias=\"COLLEGE_END\")
    lunch_start: str = Field(default=\"13:00\", alias=\"LUNCH_START\")
    lunch_end: str = Field(default=\"14:00\", alias=\"LUNCH_END\")
    attendance_safe: int = Field(default=75, alias=\"ATTENDANCE_SAFE\")
    attendance_warning: int = Field(default=65, alias=\"ATTENDANCE_WARNING\")
    max_upload_mb: int = Field(default=10, alias=\"MAX_UPLOAD_MB\")
    allowed_extensions: str = Field(default=\".pdf,.csv\", alias=\"ALLOWED_EXTENSIONS\")

    class Config:
        env_file = Path(__file__).resolve().parents[2] / \".env\"
        env_file_encoding = \"utf-8\"
        case_sensitive = False


settings = Settings()

# Derived constants for easy import
COLLEGE_START_HOUR = int(settings.college_start.split(\":\")[0])
COLLEGE_END_HOUR = int(settings.college_end.split(\":\")[0])
LUNCH_START_HOUR = int(settings.lunch_start.split(\":\")[0])
LUNCH_END_HOUR = int(settings.lunch_end.split(\":\")[0])

DAYS_ORDER = [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"]
DAY_TO_INT = {d: i for i, d in enumerate(DAYS_ORDER)}
"@ | Set-Content -Path "$b\config.py" -Encoding UTF8
Write-Host "Created: $b\config.py"

# ===== database.py =====
@"
\"\"\"Database engine, session factory, and table creation.\"\"\"
import logging
from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(settings.database_url, echo=False)


def create_db_and_tables() -> None:
    \"\"\"Create all tables defined in SQLModel metadata.\"\"\"
    logger.info(\"Creating database tables...\")
    SQLModel.metadata.create_all(engine)
    logger.info(\"Tables created.\")


def get_session() -> Session:
    \"\"\"FastAPI dependency: yields a session and ensures close.\"\"\"
    with Session(engine) as session:
        yield session


@contextmanager
def session_scope():
    \"\"\"Context manager for scripts / non-FastAPI code.\"\"\"
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
"@ | Set-Content -Path "$b\database.py" -Encoding UTF8
Write-Host "Created: $b\database.py"

# ===== models.py =====
@"
\"\"\"SQLModel tables for ClassPilot.\"\"\"
from datetime import date, time
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from enum import Enum


class AttendanceStatus(str, Enum):
    PRESENT = \"Present\"
    ABSENT = \"Absent\"
    CANCELLED = \"Cancelled\"


class Course(SQLModel, table=True):
    __tablename__ = \"course\"
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    name: str
    semester: int
    branch: str
    is_elective: bool = False
    is_extra: bool = False

    attendance_records: List[\"AttendanceRecord\"] = Relationship(back_populates=\"course\")


class AttendanceRecord(SQLModel, table=True):
    __tablename__ = \"attendance_record\"
    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key=\"course.id\", index=True)
    date: date
    status: AttendanceStatus

    course: Course = Relationship(back_populates=\"attendance_records\")


class TimetableSlot(SQLModel, table=True):
    __tablename__ = \"timetable_slot\"
    id: Optional[int] = Field(default=None, primary_key=True)
    day: str = Field(index=True)  # Mon, Tue, ...
    start_time: time
    end_time: time
    room: str
    course_code: str = Field(index=True)
    branch_or_program: str
    semester: int


class UserProfile(SQLModel, table=True):
    __tablename__ = \"user_profile\"
    id: Optional[int] = Field(default=None, primary_key=True)
    semester: int
    branch: str
    elective_codes: List[str] = Field(default=[], sa_column=Column(JSON))


class ExamSeating(SQLModel, table=True):
    __tablename__ = \"exam_seating\"
    id: Optional[int] = Field(default=None, primary_key=True)
    roll_start_prefix: str = Field(index=True)
    roll_start_num: int = Field(index=True)
    roll_end_num: int = Field(index=True)
    room: str
    exam_date: date
    start_time: time
    end_time: time
    course_code: str
"@ | Set-Content -Path "$b\models.py" -Encoding UTF8
Write-Host "Created: $b\models.py"

# ===== main.py =====
@"
\"\"\"FastAPI application entry point.\"\"\"
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_and_tables
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(\"Starting up...\")
    create_db_and_tables()
    yield
    logger.info(\"Shutting down...\")


app = FastAPI(title=\"ClassPilot API\", version=\"0.1.0\", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[\"http://localhost:5173\"],
    allow_credentials=True,
    allow_methods=[\"*\"],
    allow_headers=[\"*\"],
)


@app.get(\"/health\")
def health_check():
    return {\"status\": \"ok\"}


# Router imports (Phase 2+ will uncomment)
# from routes import attendance, timetable, schedule, rooms, exam, profile
# app.include_router(attendance.router, prefix=\"/attendance\", tags=[\"Attendance\"])
# app.include_router(timetable.router, prefix=\"/timetable\", tags=[\"Timetable\"])
# app.include_router(schedule.router, prefix=\"/schedule\", tags=[\"Schedule\"])
# app.include_router(rooms.router, prefix=\"/rooms\", tags=[\"Rooms\"])
# app.include_router(exam.router, prefix=\"/exam\", tags=[\"Exam\"])
# app.include_router(profile.router, prefix=\"/profile\", tags=[\"Profile\"])


if __name__ == \"__main__\":
    import uvicorn
    uvicorn.run(\"main:app\", host=\"0.0.0.0\", port=8000, reload=True)
"@ | Set-Content -Path "$b\main.py" -Encoding UTF8
Write-Host "Created: $b\main.py"

# ===== seed.py =====
@"
\"\"\"Seed script: loads sample timetable, courses, attendance, and exam data.\"\"\"
import sys
import logging
from pathlib import Path
from datetime import date, time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import session_scope
from models import (
    Course, AttendanceRecord, AttendanceStatus,
    TimetableSlot, UserProfile, ExamSeating
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_courses(session):
    courses = [
        Course(code=\"CS301\", name=\"Database Systems\", semester=5, branch=\"CSE\", is_elective=False),
        Course(code=\"CS302\", name=\"Computer Networks\", semester=5, branch=\"CSE\", is_elective=False),
        Course(code=\"CS303\", name=\"Operating Systems\", semester=5, branch=\"CSE\", is_elective=False),
        Course(code=\"CS304\", name=\"Machine Learning\", semester=5, branch=\"CSE\", is_elective=True),
        Course(code=\"MA201\", name=\"Discrete Mathematics\", semester=3, branch=\"CSE\", is_elective=False),
        Course(code=\"EE101\", name=\"Basic Electrical\", semester=1, branch=\"EE\", is_elective=False),
    ]
    for c in courses:
        session.merge(c)
    session.flush()
    logger.info(f\"Seeded {len(courses)} courses\")
    return {c.code: c.id for c in courses}


def seed_attendance(session, course_ids):
    today = date.today()
    records = [
        AttendanceRecord(course_id=course_ids[\"CS301\"], date=date(today.year, today.month, 1), status=AttendanceStatus.PRESENT),
        AttendanceRecord(course_id=course_ids[\"CS301\"], date=date(today.year, today.month, 3), status=AttendanceStatus.PRESENT),
        AttendanceRecord(course_id=course_ids[\"CS301\"], date=date(today.year, today.month, 5), status=AttendanceStatus.ABSENT),
        AttendanceRecord(course_id=course_ids[\"CS301\"], date=date(today.year, today.month, 8), status=AttendanceStatus.PRESENT),
        AttendanceRecord(course_id=course_ids[\"CS301\"], date=date(today.year, today.month, 10), status=AttendanceStatus.CANCELLED),
        AttendanceRecord(course_id=course_ids[\"CS302\"], date=date(today.year, today.month, 2), status=AttendanceStatus.PRESENT),
        AttendanceRecord(course_id=course_ids[\"CS302\"], date=date(today.year, today.month, 4), status=AttendanceStatus.ABSENT),
        AttendanceRecord(course_id=course_ids[\"CS302\"], date=date(today.year, today.month, 6), status=AttendanceStatus.ABSENT),
        AttendanceRecord(course_id=course_ids[\"CS302\"], date=date(today.year, today.month, 9), status=AttendanceStatus.PRESENT),
        AttendanceRecord(course_id=course_ids[\"CS303\"], date=date(today.year, today.month, 1), status=AttendanceStatus.PRESENT),
        AttendanceRecord(course_id=course_ids[\"CS303\"], date=date(today.year, today.month, 3), status=AttendanceStatus.PRESENT),
        AttendanceRecord(course_id=course_ids[\"CS303\"], date=date(today.year, today.month, 5), status=AttendanceStatus.PRESENT),
    ]
    for r in records:
        session.add(r)
    logger.info(f\"Seeded {len(records)} attendance records\")


def seed_timetable(session):
    slots = [
        # Mon
        TimetableSlot(day=\"Mon\", start_time=time(9, 0), end_time=time(10, 0), room=\"L-101\", course_code=\"CS301\", branch_or_program=\"CSE\", semester=5),
        TimetableSlot(day=\"Mon\", start_time=time(10, 0), end_time=time(11, 0), room=\"L-102\", course_code=\"CS302\", branch_or_program=\"CSE\", semester=5),
        TimetableSlot(day=\"Mon\", start_time=time(11, 15), end_time=time(12, 15), room=\"L-101\", course_code=\"CS303\", branch_or_program=\"CSE\", semester=5),
        TimetableSlot(day=\"Mon\", start_time=time(14, 0), end_time=time(15, 0), room=\"CR-201\", course_code=\"CS304\", branch_or_program=\"CSE\", semester=5),
        # Tue
        TimetableSlot(day=\"Tue\", start_time=time(9, 0), end_time=time(10, 0), room=\"L-102\", course_code=\"CS302\", branch_or_program=\"CSE\", semester=5),
        TimetableSlot(day=\"Tue\", start_time=time(10, 0), end_time=time(11, 0), room=\"L-101\", course_code=\"CS301\", branch_or_program=\"CSE\", semester=5),
        TimetableSlot(day=\"Tue\", start_time=time(11, 15), end_time=time(12, 15), room=\"L-201\", course_code=\"CS303\", branch_or_program=\"CSE\", semester=5),
        # Wed
        TimetableSlot(day=\"Wed\", start_time=time(9, 0), end_time=time(10, 0), room=\"L-101\", course_code=\"CS303\", branch_or_program=\"CSE\", semester=5),
        TimetableSlot(day=\"Wed\", start_time=time(10, 0), end_time=time(11, 0), room=\"CR-201\", course_code=\"CS304\", branch_or_program=\"CSE\", semester=5),
        # Thu
        TimetableSlot(day=\"Thu\", start_time=time(9, 0), end_time=time(10, 0), room=\"L-102\", course_code=\"CS301\", branch_or_program=\"CSE\", semester=5),
        TimetableSlot(day=\"Thu\", start_time=time(10, 0), end_time=time(11, 0), room=\"L-101\", course_code=\"CS302\", branch_or_program=\"CSE\", semester=5),
        # Fri
        TimetableSlot(day=\"Fri\", start_time=time(9, 0), end_time=time(10, 0), room=\"L-101\", course_code=\"CS303\", branch_or_program=\"CSE\", semester=5),
        TimetableSlot(day=\"Fri\", start_time=time(10, 0), end_time=time(11, 0), room=\"L-102\", course_code=\"CS301\", branch_or_program=\"CSE\", semester=5),
    ]
    for s in slots:
        session.add(s)
    logger.info(f\"Seeded {len(slots)} timetable slots\")


def seed_profile(session):
    profile = UserProfile(id=1, semester=5, branch=\"CSE\", elective_codes=[\"CS304\"])
    session.merge(profile)
    logger.info(\"Seeded user profile\")


def seed_exams(session):
    exams = [
        ExamSeating(roll_start_prefix=\"23BCS\", roll_start_num=1, roll_end_num=50, room=\"L-101\", exam_date=date(2026, 12, 15), start_time=time(9, 0), end_time=time(12, 0), course_code=\"CS301\"),
        ExamSeating(roll_start_prefix=\"23BCS\", roll_start_num=51, roll_end_num=100, room=\"L-102\", exam_date=date(2026, 12, 15), start_time=time(9, 0), end_time=time(12, 0), course_code=\"CS301\"),
        ExamSeating(roll_start_prefix=\"23BCS\", roll_start_num=1, roll_end_num=100, room=\"CR-201\", exam_date=date(2026, 12, 17), start_time=time(9, 0), end_time=time(12, 0), course_code=\"CS302\"),
        ExamSeating(roll_start_prefix=\"23BCS\", roll_start_num=1, roll_end_num=100, room=\"L-201\", exam_date=date(2026, 12, 19), start_time=time(14, 0), end_time=time(17, 0), course_code=\"CS303\"),
        ExamSeating(roll_start_prefix=\"23BCS\", roll_start_num=1, roll_end_num=30, room=\"CR-202\", exam_date=date(2026, 12, 21), start_time=time(9, 0), end_time=time(12, 0), course_code=\"CS304\"),
    ]
    for e in exams:
        session.add(e)
    logger.info(f\"Seeded {len(exams)} exam seating records\")


def main():
    with session_scope() as session:
        course_ids = seed_courses(session)
        seed_attendance(session, course_ids)
        seed_timetable(session)
        seed_profile(session)
        seed_exams(session)
    logger.info(\"Seeding complete.\")


if __name__ == \"__main__\":
    main()
"@ | Set-Content -Path "$b\scripts\seed.py" -Encoding UTF8
Write-Host "Created: $b\scripts\seed.py"

Write-Host "`n✅ All Phase 1 backend files created!" -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "  1. cd $root"
Write-Host "  2. pip install -r requirements.txt"
Write-Host "  3. cd backend\backend"
Write-Host "  4. python scripts\seed.py"
Write-Host "  5. uvicorn main:app --reload --port 8000"
Write-Host "  6. curl http://localhost:8000/health"