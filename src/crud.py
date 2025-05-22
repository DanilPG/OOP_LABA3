from sqlalchemy.orm import Session
from datetime import datetime
from . import models

def get_todolist(db: Session, todolist_id: int):
    return db.query(models.TodoList).filter(
        models.TodoList.id == todolist_id,
        models.TodoList.deleted_at == None
    ).first()

def create_todolist(db: Session, name: str):
    db_todolist = models.TodoList(name=name, done_count=0, total_count=0)
    db.add(db_todolist)
    db.commit()
    db.refresh(db_todolist)
    return db_todolist

def get_items(db: Session, todolist_id: int):
    return db.query(models.Item).filter(
        models.Item.todolist_id == todolist_id,
        models.Item.deleted_at == None
    ).all()

def create_item(db: Session, todolist_id: int, name: str, text: str):
    db_item = models.Item(todolist_id=todolist_id, name=name, text=text, is_done=False)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    update_todolist_counters(db, todolist_id)
    return db_item

def update_item(db: Session, item_id: int, name: str, text: str, is_done: bool):
    db_item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.deleted_at == None
    ).first()
    if db_item:
        db_item.name = name
        db_item.text = text
        db_item.is_done = is_done
        db.commit()
        db.refresh(db_item)
        update_todolist_counters(db, db_item.todolist_id)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(
        models.Item.id == item_id,
        models.Item.deleted_at == None
    ).first()
    if db_item:
        db_item.deleted_at = datetime.utcnow()
        db.commit()
        update_todolist_counters(db, db_item.todolist_id)
    return db_item

def delete_todolist(db: Session, todolist_id: int):
    todolist = get_todolist(db, todolist_id)
    if todolist:
        todolist.deleted_at = datetime.utcnow()
        db.commit()
    return todolist

def update_todolist_counters(db: Session, todolist_id: int):
    total = db.query(models.Item).filter(
        models.Item.todolist_id == todolist_id,
        models.Item.deleted_at == None
    ).count()

    done = db.query(models.Item).filter(
        models.Item.todolist_id == todolist_id,
        models.Item.is_done == True,
        models.Item.deleted_at == None
    ).count()

    todolist = db.query(models.TodoList).filter(
        models.TodoList.id == todolist_id,
        models.TodoList.deleted_at == None
    ).first()

    if todolist:
        todolist.total_count = total
        todolist.done_count = done
        db.commit()
