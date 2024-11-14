from fastapi import FastAPI,Depends, Path,status
from typing import Annotated
from sqlalchemy.orm import Session
import models
from pydantic import Field,BaseModel
from models import Todos
from database import engine,SessionLocal
from todo_app_routers import auth                    #importiamo il file auth.py dalla cartella routers

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)                 #includiamo dei router all'applicazione principale(altrimenti all'esecuzione non vengono visti), in questo caso il router del file auth

class TodoRequest(BaseModel):
    title: str  = Field(min_length=3)
    description: str  =Field(min_length=3,max_length=100)
    priority: int    =Field(gt=0,lt=6)
    complete: bool

def get_db():
    db=SessionLocal()
    try:
        yield db            #lo yield fa si che solo il codice prima ed incluso nello yield venga eseguito prima di avere una risposta
    finally:
        db.close()          #il finally esegue il codice quando la risposta è ricevuta (connessione con database viene aperta e quando vengono sono state eseguite le operazioni e ritornata una risposta la connessione viene chiusa)


db_dependency=Annotated[Session,Depends(get_db)]

@app.get("/",status_code=status.HTTP_200_OK)            #explicitating what status code to return if the function is succesful
async def get_db(db:db_dependency):
    return db.query(Todos).all()

@app.post("/todo",status_code=status.HTTP_201_CREATED)
async def post_db(db:db_dependency,todo_request:TodoRequest):
    todo_model=Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()


@app.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def get_record_by_id(db:db_dependency, todo_id: int = Path(gt=0) ):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()               #telling it to stop at the first value to improve performances
    if todo_model!=None:
        return todo_model
    raise status.HTTP_404_NOT_FOUND


@app.put("/todo/{todo_id}",status_code=status.HTTP_202_ACCEPTED)
async def db_update(db:db_dependency,todo_request:TodoRequest,todo_id:int = Path(gt=0)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model==None:
        raise status.HTTP_404_NOT_FOUND
    
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_model.complete

    db.add(todo_model)
    db.commit()

@app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def db_delete(db:db_dependency,todo_id:int = Path(gt=0)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model==None:
        raise status.HTTP_404_NOT_FOUND
    
    db.query(Todos).filter(db.id==todo_id).delete()
    db.commit()