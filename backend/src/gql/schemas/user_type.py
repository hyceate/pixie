from ariadne_graphql_modules import gql

user_type_defs = gql(
    """
    type User {
        id: ID!
        username: String!
        posts: [Post!]!
    }

    extend type Query {
        getUser(id: ID!): User
        getUsers: [User!]!
    }

    extend type Mutation {
        createUser(username: String!): User
    }
    """
)
