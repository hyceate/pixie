# gql/resolvers/user_resolvers.py
from ariadne import QueryType, MutationType

query = QueryType()
mutation = MutationType()

@query.field("getUser")
def resolve_get_user(_, info, id):
    
    pass

@query.field("getUsers")
def resolve_get_users(_, info, id):
    
    pass

@mutation.field("createUser")
def resolve_create_user(_, info, name):
   
    pass

# Export the bindables
user_query = query
user_mutation = mutation
