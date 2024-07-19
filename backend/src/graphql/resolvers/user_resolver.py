from ..schema.user import UserType

def resolve_users(root, info):
   
    return [
        UserType(id=1, username="user1", email="user1@example.com"),
        UserType(id=2, username="user2", email="user2@example.com"),
    ]