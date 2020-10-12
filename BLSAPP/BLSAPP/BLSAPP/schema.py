import graphene

import api.schema 


class Query(api.schema.Query, graphene.ObjectType):
    # This class extends all abstract apps level Queries and graphene.ObjectType
    pass

# Mutation for sending the data to the server.
class Mutation(api.schema.Mutation, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query , mutation=Mutation)