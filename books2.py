from fastapi import FastAPI,Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app=FastAPI()

class book():
    id: int
    title:str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating


class book_model(BaseModel):
    id: Optional[int] = Field(description="ID is not required",default=None)
    title: str =Field(min_length=1,max_length=100)
    author: str =Field(min_length=1,max_length=100)
    description: str =Field(min_length=1,max_length=100)
    rating: int =Field(gt=0,lt=6)

    model_config= {
        "json_schema_extra":{
            "example":{
                "title": "example",
                "author": "example",
                "description": "example",
                "rating": 0
            }
        }
    }


BOOKS=[
    book(1,'title 1','author 1', 'description 1',5),
    book(2,'title 2','author 2', 'description 2',3),
    book(3,'title 3','author 1', 'description 3',2),
    book(4,'title 4','author 3', 'description 4',3),
    book(5,'title 5','author 5', 'description 5',4),
    book(6,'title 6','author 2', 'description 6',1),
    book(7,'title 7','author 4', 'description 7',5),
]

@app.post("/books/create_book",status_code=status.HTTP_200_OK)          #il secondo argomento qua viene da starlet ed è il codice che esce quando la tua funzione ha finito con successo
async def get_book(book_request: book_model):
    new_book=book(**book_request.model_dump())
    new_book.id=id_sorting()
    BOOKS.append(new_book)

@app.get("/books")
async def get_all_book():
    return BOOKS

def id_sorting():
    id=0
    if len(BOOKS)==0:
        id=1
    else: id=BOOKS[-1].id + 1
    return id

@app.put("/books/update")
async def update_books(book_given:book_model):
    for i in range(len(BOOKS)):
        if book_given.id==i:
            BOOKS[i]=book_given

@app.get("/books/rating/")
async def book_rating(rating: str = Query(gt=0,lt=6)):      #query param validation
    book_to_return=[]
    for book in BOOKS:
        if book.rating==rating:
            book_to_return.append(book)

@app.get("/books/{author}")
async def book_rating(author: str = Path(min_length=1, max_length=100)):    #query param validation
    book_to_return=[]
    for book in BOOKS:
        if book.author==author:
            book_to_return.append(book)
    raise HTTPException(status_code=404, detail="author not found")                  #status code che puoi far uscire con raise per vari motivi(es qualcosa non trovato)
