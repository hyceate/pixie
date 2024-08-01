from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .sql_models.user import User
from .sql_models.images import Images
from .sql_models.comment import Comment
from .sql_models.post import Post

__all__ = ["Base", "User", "Post", "Comment", "Images"]