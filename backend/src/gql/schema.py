# schema.py
from ariadne import make_executable_schema
from gql.schemas.user_type import user_type_defs
from gql.schemas.post_type import post_type_defs
from gql.resolvers.user_resolvers import user_query, user_mutation
from gql.resolvers.post_resolvers import post_query, post_mutation

# Combine all type definitions
type_defs = [
    user_type_defs,
    post_type_defs
]

# Combine all bindables (resolvers)
bindables = [
    user_query,
    user_mutation,
    post_query,
    post_mutation
]

# Create the schema
schema = make_executable_schema(type_defs, bindables)
