# init_db.py
from src.database import engine, Base
from src.models import Campaign, Post # Import models so Base "knows" about them

def init_db():
    print("⏳ Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    init_db()