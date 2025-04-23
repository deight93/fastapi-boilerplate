from sqladmin import ModelView

from app.models.admin import Admin


class AdminTable(ModelView, model=Admin):
    name = "Admin"
    name_plural = "Admin"
    icon = "fa-solid fa-book"
    can_create = False
    can_delete = False
    can_edit = False
    column_list = [c.name for c in Admin.__table__.c]
