from ariadne_graphql_modules import gql

comment_type_defs = gql(
  """
  type Comment{
    id: ID!
    content: String!
  }

  extend type Query{
    getComment(id: ID!): Comment
  }

  input CommentInput{
    commenter: String
  }
  
  extend type Mutation{
    createComment(input:CommentInput!): CreateResponse
  }
  """
)