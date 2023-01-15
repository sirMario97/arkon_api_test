import graphene
import puntos_wifi.schema

class Query(puntos_wifi.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)