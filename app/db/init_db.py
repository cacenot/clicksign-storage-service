from sqlalchemy.orm import Session

from app.models import Folder
from ..crud import folder as crud


def init_db(db: Session) -> None:
    root_folder = crud.get_root_folder(db)
    if not root_folder:
        root_folder = Folder(name="root")
        db.add(root_folder)
        db.commit()
