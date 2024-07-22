from ariadne import QueryType, MutationType

query = QueryType()
mutation = MutationType()

@query.field("getPost")
def resolve_get_post(_, info, id):
   
    pass

@query.field("getPosts")
def resolve_get_posts(_, info, id):
    
    pass

@mutation.field("createPost")
def resolve_create_Post(_, info, name):
    
    pass

# Export the bindables
post_query = query
post_mutation = mutation
