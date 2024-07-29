from ariadne import QueryType, MutationType

query = QueryType()
mutation = MutationType()

@query.field("getComment")
def resolve_getComment():
  pass


# export bindables
comment_query = query
comment_mutation = mutation