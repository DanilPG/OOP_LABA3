from pydantic import BaseModel
from typing import List, Optional

class TodoListCreate(BaseModel):
    name: str

class TodoList(BaseModel):
    id: int
    name: str
    done_count: int
    total_count: int
    progress: float = 0.0  # вычисляемое поле для процента
    items: List[str] = []

    class Config:
        orm_mode = True

class ItemCreate(BaseModel):
    name: str
    text: str

class Item(BaseModel):
    id: int
    name: str
    text: str
    is_done: bool
    todolist_id: int

    class Config:
        orm_mode = True
