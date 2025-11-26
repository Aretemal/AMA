from fastapi import FastAPI
from fastapi.responses import HTMLResponse
 
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String
 
# строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
 
# создаем движок SqlAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#создаем базовый класс для моделей
class Base(DeclarativeBase): pass
 
# создаем модель, объекты которой будут храниться в бд
class Person(Base):
    __tablename__ = "people"
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer,)
 
# создаем таблицы
Base.metadata.create_all(bind=engine)
 
# приложение, которое ничего не делает
app = FastAPI()
 
@app.get("/")
def read_root():
    html_content = "<h2>Hello METANIT.COM!</h2>"
    return HTMLResponse(content=html_content)