from ariadne_graphql_modules import gql

post_type_defs = gql(
    """
    type Post {
        id: ID!
        description: String!
        imageUrl: String
        author: User!
        createdAt: String!
        updatedAt: String!
    }

    type Query {
        getPost(id: ID!): Post
        getPosts: [Post!]!
    }

    input CreateInput {
        description: String!
        imageUrl: String
        authorId: ID!
    }

    type CreateResponse{
        success: Boolean!
        message: String!
    }
    type Mutation {
        createPost(input: CreateInput!): CreateResponse!
    }
    """
)
