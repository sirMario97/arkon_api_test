import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q
from .models import Accesos

#Se crea un objeto DjangoObjectType para que graphene pueda interpretarlo correctamente
class AccesoType(DjangoObjectType):
    class Meta:
        model = Accesos
        exclude = ['id']

# Clase que hereda de graphene, contiene los atributos y funciones para resolver las peticiones de tipo graphQL
class Query(graphene.ObjectType):
    # Variable que interpreetará la lista de registros entregados por django
    accesos = graphene.List(AccesoType, search=graphene.String())
    ver_acceso_id = graphene.List(AccesoType, search=graphene.String())

    #En caso de que la petición indique buscar por atributos específicos, esta funcion filtrará o entregará la lista completa
    def resolve_accesos(self, info, search=None):
        if search:#Si existen atributos para filtrar
            filter = (
                Q(id_wifi__icontains=search) |
                Q(programa__icontains=search) |
                Q(fecha_instalacion__icontains=search) |
                Q(latitud__icontains=search) |
                Q(longitud__icontains=search) |
                Q(colonia__icontains=search) |
                Q(alcaldia__icontains=search) 
            )
            return Accesos.objects.filter(filter)#entrega lista de Accesos filtrada
        return Accesos.objects.all()#entrega lista de Accesos completa

    #En caso de que la petición indique buscar por id, esta funcion filtrará o entregará la lista completa
    def resolve_accesos(self, info, search=None):
        if search:#Si existen atributos para filtrar
            filter = (
                Q(id_wifi__icontains=search) |
                Q(programa__icontains=search) |
                Q(fecha_instalacion__icontains=search) |
                Q(latitud__icontains=search) |
                Q(longitud__icontains=search) |
                Q(colonia__icontains=search) |
                Q(alcaldia__icontains=search) 
            )
            return Accesos.objects.filter(filter)#entrega lista de Accesos filtrada
        return Accesos.objects.all()#entrega lista de Accesos completa
#schema = graphene.Schema(query=Query)