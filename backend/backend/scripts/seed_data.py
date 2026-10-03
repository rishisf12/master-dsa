import sys
from pathlib import Path
from datetime import datetime, timedelta
import calendar

# Add current directory (inner backend) to path
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from sqlmodel import Session, select
from app.db.session import engine
from app.models.month import Month
from app.models.day import Day
from app.core.constants import MONTHS
from app.utils.logger import logger
from dotenv import load_dotenv

# ✅ Load .env file from the correct location
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)


def seed_database():
    """Seed the database with initial months and days."""
    try:
        with Session(engine) as session:
            logger.info("🌱 Seeding initial data...")
            
            # Check if data already exists
            existing_months = session.exec(select(Month)).all()
            if existing_months:
                logger.info("📊 Data already exists. Skipping seed.")
                return True
            
            # Create months
            for month_data in MONTHS:
                month = Month(
                    name=month_data["name"],
                    year=month_data["year"],
                    month_number=month_data["month"]
                )
                session.add(month)
                session.flush()
                
                # Generate days for this month
                start_date = datetime(month_data["year"], month_data["month"], 1)
                
                if month_data["month"] == 12:
                    end_date = datetime(month_data["year"] + 1, 1, 1)
                else:
                    end_date = datetime(month_data["year"], month_data["month"] + 1, 1)
                
                current_date = start_date
                week_counter = 0
                
                while current_date < end_date:
                    if current_date.weekday() == 0:
                        week_counter += 1
                    
                    day = Day(
                        date=current_date,
                        day_of_week=calendar.day_name[current_date.weekday()],
                        week_number=week_counter,
                        day_number=current_date.day,
                        month_id=month.id
                    )
                    session.add(day)
                    current_date += timedelta(days=1)
            
            session.commit()
            logger.info("✅ Seed data inserted successfully!")
            return True
            
    except Exception as e:
        logger.error(f"❌ Failed to seed database: {str(e)}")
        return False


if __name__ == "__main__":
    print("🚀 Seeding Master DSA Database...")
    success = seed_database()
    if success:
        print("✅ Database seeded successfully!")
    else:
        print("❌ Database seeding failed!")
        sys.exit(1)