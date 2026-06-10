from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Todo
from ..schemas import TodoCreate, DeleteIds

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/")
def get_todos():

    db: Session = SessionLocal()

    todos = db.query(Todo).all()

    db.close()

    return todos


@router.post("/")
def create_todo(todo: TodoCreate):

    db: Session = SessionLocal()

    new_todo = Todo(title=todo.title)

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    db.close()

    return new_todo


@router.delete("/{todo_id}")
def delete_todo(todo_id: int):

    db: Session = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        db.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    db.close()

    return {"ok": True}


@router.delete("/")
def delete_todos(ids: DeleteIds):

    db: Session = SessionLocal()
    deleted = db.query(Todo).filter(Todo.id.in_(ids.ids)).delete(synchronize_session=False)
    db.commit()
    db.close()

    return {"deleted": deleted}