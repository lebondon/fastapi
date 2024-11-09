from fastapi import Body,FastAPI

app=FastAPI()

BOOKS = [
    {'title':'Title One','author': 'Author One','category':'science' },
    {'title':'Title Two','author': 'Author Two','category':'math' },
    {'title':'Title Three','author': 'Author Three','category':'science' },
    {'title':'Title Four','author': 'Author Four','category':'physics' },
    {'title':'Title Five','author': 'Author Five','category':'science' },
    {'title':'Title Six','author': 'Author three','category':'math' }
]

@app.get("/books")
def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
        
@app.get("/books/{author}/")
async def read_author_category_by_query(author: str, category: str):
    book_to_return=[]
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold() and book.get('category').casefold() == category.casefold():
            book_to_return.append(book)
    return book_to_return

@app.post("books/create_new_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.post("books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title'):
            BOOKS[i]=updated_book    
