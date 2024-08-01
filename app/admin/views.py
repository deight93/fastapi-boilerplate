from sqladmin import ModelView

from app.models.users import Users


class UsersAdmin(ModelView, model=Users):
    name = "Users"
    name_plural = "User"
    icon = "fa-solid fa-book"
    can_create = False
    can_delete = False
    can_edit = False
    column_list = [c.name for c in Users.__table__.c]
