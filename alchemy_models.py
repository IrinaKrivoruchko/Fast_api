from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


DATABASE_URL = "sqlite:///./fs.db"

# init session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, unique=True, index=True)
    brand = Column(String, index=True)
    price = Column(Integer, index=True)
    category = Column(String, index=True)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)


Base.metadata.create_all(bind=engine)


def get_db():
    """
    Get the database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
