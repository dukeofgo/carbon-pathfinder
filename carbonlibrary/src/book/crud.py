from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from . import schemas, models
import base64

def get_book_by_id(db: Session, book_id: int):
    return db.execute(select(models.Book).where(models.Book.id == book_id)).scalars().first()

def get_book_by_isbn(db: Session, isbn: str):   
    return db.execute(select(models.Book).where(models.Book.isbn == isbn)).scalars().first()

def get_book_by_isbn_or_id(db: Session, isbn_or_id: str):
    return db.execute(select(models.Book).where(or_(models.Book.isbn == isbn_or_id, models.Book.id == int(isbn_or_id)))).scalars().first()

def get_books(db: Session, skip: int = 0, limit: int = 20):
    return db.execute(select(models.Book).offset(skip).limit(limit)).scalars().all()

def create_book(db: Session, book: schemas.BookCreate):
    #convert pydantic model to python dict
    book_dict = book.model_dump(exclude_unset=True)
    #unpack book_dict into model
    db_book = models.Book(**book_dict)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book

def update_book(db: Session, book_id: int, book: schemas.BookUpdate | None = None):
    query_book = get_book_by_id(db=db, book_id=book_id)

    if book:
        #convert pydantic model to python dict
        update_data = book.model_dump(exclude_unset=True)
        
        """If fields have been modified, setattr, if not then skip setattr"""
        if update_data:
            for key, value in update_data.items():
                setattr(query_book, key, value)

    db.add(query_book)
    db.commit()
    db.refresh(query_book)

    return query_book

def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db=db, book_id=book_id)

    db.delete(db_book)
    db.commit()

    return {"message": "Book deleted successfully"}

def update_book_cover(img_content: bytes, book_id: int, db: Session):
    db_book = get_book_by_id(book_id=book_id, db=db)

    # RAW BINARY DATA is difficult to handle and not compatible with JSON, so it is easier to convert RAW BINARY to utf-8 string first, if you want to store image in database
    # Encode RAW BINARY to Base64 bytes(b'abcdef'), and convert to UTF-8 string ("ghijkl")
    encoded_image_data = base64.b64encode(img_content).decode('utf-8')
    # Store the encoded data to database of db_book
    db_book.cover_image = encoded_image_data
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return {"message": "success upload"}
