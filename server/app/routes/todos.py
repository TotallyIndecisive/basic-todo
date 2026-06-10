from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Todo
from app.schemas import TodoCreate, DeleteIds

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/")
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos


@router.post("/")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(title=todo.title)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"ok": True}


@router.delete("/")
def delete_todos(ids: DeleteIds, db: Session = Depends(get_db)):
    deleted = db.query(Todo).filter(Todo.id.in_(ids.ids)).delete(synchronize_session=False)
    db.commit()
    return {"deleted": deleted}
