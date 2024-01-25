from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///fastapi.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class LaptopDB(Base):
    __tablename__ = 'laptop'
    brand = Column('Brand', String(50))
    model = Column('Model', String, unique=True, primary_key=True)
    price = Column('Price', Float)
    battery_capacity = Column("Battery capacity", Integer)

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def delete_laptop_by_model(db_session, model):
    laptop = db_session.query(LaptopDB).filter(LaptopDB.model == model).first()
    if laptop:
        db_session.delete(laptop)
        db_session.commit()
        return True
    return False
