from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQL_ALCHEMY_DATABASE_URL='sqlite:///todo.db'

engine=create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base=declarative_base()