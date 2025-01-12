from sqladmin import ModelView

from app.models.user import User


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "User"
    icon = "fa-solid fa-book"
    can_create = False
    can_delete = False
    can_edit = False
    column_list = [c.name for c in User.__table__.c]
