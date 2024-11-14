from fastapi import APIRouter,Depends, Path,status
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import Field,BaseModel
from models import Todos
from database import SessionLocal               

router=APIRouter()
            
class TodoRequest(BaseModel):
    title: str  = Field(min_length=3)
    description: str  =Field(min_length=3,max_length=100)
    priority: int    =Field(gt=0,lt=6)
    complete: bool

def get_db():
    db=SessionLocal()
    try:
        yield db            
    finally:
        db.close()          


db_dependency=Annotated[Session,Depends(get_db)]

@router.get("/",status_code=status.HTTP_200_OK)            
async def get_db(db:db_dependency):
    return db.query(Todos).all()

@router.post("/todo",status_code=status.HTTP_201_CREATED)
async def post_db(db:db_dependency,todo_request:TodoRequest):
    todo_model=Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()


@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def get_record_by_id(db:db_dependency, todo_id: int = Path(gt=0) ):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()               
    if todo_model!=None:
        return todo_model
    raise status.HTTP_404_NOT_FOUND


@router.put("/todo/{todo_id}",status_code=status.HTTP_202_ACCEPTED)
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

@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def db_delete(db:db_dependency,todo_id:int = Path(gt=0)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model==None:
        raise status.HTTP_404_NOT_FOUND
    
    db.query(Todos).filter(db.id==todo_id).delete()
    db.commit()