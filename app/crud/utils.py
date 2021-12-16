from sqlalchemy.orm import Session

from ..models import Folder


def get_folder_path(db: Session, folder_id):
    beginning_getter = db.query(Folder).\
        filter(Folder.id == folder_id, Folder.parent_id != None).cte(name='parent_for', recursive=True) # noqa

    with_recursive = beginning_getter.union_all(
        db.query(Folder).filter(Folder.id == beginning_getter.c.parent_id, Folder.parent_id != None) # noqa
    )

    parent_folders = db.query(with_recursive).all()
    path = ""
    for folder in parent_folders:
        path = f"/{folder.id}{path}"
    path = f"{path}/"

    return path
