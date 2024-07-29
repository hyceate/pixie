from ariadne import gql

shared_type_defs = gql("""
    type CreateResponse {
        success: Boolean!
        message: String!
    }
""")