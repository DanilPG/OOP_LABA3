from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from . import crud, schemas, models, database

router = APIRouter()

@router.post("/todolists/", response_model=schemas.TodoList)
def create_todolist(name: str, db: Session = Depends(database.get_db)):
    todolist = crud.create_todolist(db, name)
    # добавляем progress в ответ
    progress = (todolist.done_count / todolist.total_count * 100) if todolist.total_count > 0 else 0
    return schemas.TodoList.from_orm(todolist).copy(update={"progress": progress})

@router.get("/todolists/", response_model=List[schemas.TodoList])
def get_todolists(db: Session = Depends(database.get_db)):
    todolists = db.query(models.TodoList).filter(models.TodoList.deleted_at == None).all()
    result = []
    for todolist in todolists:
        progress = (todolist.done_count / todolist.total_count * 100) if todolist.total_count > 0 else 0
        todo_schema = schemas.TodoList.from_orm(todolist).copy(update={"progress": progress})
        result.append(todo_schema)
    return result

@router.get("/todolists/{todolist_id}", response_model=schemas.TodoList)
def get_todolist(todolist_id: int, db: Session = Depends(database.get_db)):
    todolist = crud.get_todolist(db, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="TodoList not found")
    progress = (todolist.done_count / todolist.total_count * 100) if todolist.total_count > 0 else 0
    return schemas.TodoList.from_orm(todolist).copy(update={"progress": progress})

@router.post("/todolists/{todolist_id}/items/", response_model=schemas.Item)
def create_item(todolist_id: int, name: str, text: str, db: Session = Depends(database.get_db)):
    item = crud.create_item(db, todolist_id, name, text)
    return item

@router.get("/todolists/{todolist_id}/items/", response_model=List[schemas.Item])
def get_items(todolist_id: int, db: Session = Depends(database.get_db)):
    return crud.get_items(db, todolist_id)

@router.patch("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, name: str, text: str, is_done: bool, db: Session = Depends(database.get_db)):
    item = crud.update_item(db, item_id, name, text, is_done)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(database.get_db)):
    item = crud.delete_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/todolists/{todolist_id}", response_model=schemas.TodoList)
def delete_todolist(todolist_id: int, db: Session = Depends(database.get_db)):
    todolist = crud.delete_todolist(db, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="TodoList not found")
    progress = (todolist.done_count / todolist.total_count * 100) if todolist.total_count > 0 else 0
    return schemas.TodoList.from_orm(todolist).copy(update={"progress": progress})
