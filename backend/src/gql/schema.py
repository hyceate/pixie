# schema.py
from ariadne import make_executable_schema
from .schemas.shared_type import shared_type_defs
from .schemas.user_type import user_type_defs
from .schemas.post_type import post_type_defs
from .schemas.comment_type import comment_type_defs
from .resolvers.user_resolvers import user_query, user_mutation
from .resolvers.post_resolvers import post_query, post_mutation
from .resolvers.comment_resolvers import comment_query, comment_mutation

# Combine all type definitions
type_defs = [
    user_type_defs,
    post_type_defs,
    comment_type_defs,
    shared_type_defs
]

# Combine all bindables (resolvers)
bindables = [
    user_query,
    user_mutation,
    post_query,
    post_mutation,
    comment_query,
    comment_mutation
]

# Create the schema
schema = make_executable_schema(type_defs, bindables)
