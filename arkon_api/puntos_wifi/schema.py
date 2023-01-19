import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from django.db.models import Q
from .models import Accesos
from decimal import Decimal, InvalidOperation  


"""
Se crea un objeto DjangoObjectType para que graphene pueda interpretarlo correctamente
"""
class AccesoType(DjangoObjectType):
    class Meta:
        model = Accesos
        interfaces = (relay.Node, )
        filter_fields = {#Filtros para obtener consultas buscando el id o la colonia
            'id_wifi': ['exact', 'icontains', 'istartswith'],
            'colonia': ['exact', 'icontains'],
        }


"""
Calse que permite busquedas páginadas, usando la libreria de relay 
"""
class QuestionConnection(relay.Connection):
    class Meta:
        node = AccesoType


"""
Clase que permite crear las búsquedas, llamando las librerías de graphene
"""
class Query(graphene.ObjectType):
    accesos = graphene.List(AccesoType, search=graphene.String())
    accesos_cercanos = relay.ConnectionField(
        QuestionConnection, latitud=graphene.String(), longitud=graphene.String(), 
        extra_latitud=graphene.String(), extra_longitud=graphene.String(),
        menos_latitud=graphene.String(), menos_longitud=graphene.String()
    )
    accesos_paginados = relay.ConnectionField(QuestionConnection)
    ver_colonias = DjangoFilterConnectionField(AccesoType)
    ver_acceso_id = graphene.List(AccesoType, id=graphene.String())

    #Entrega una lista áginada de puntos wifi cercanos a unas cordenadas indicadas. En donde:
    #longitud: valor base, latitud: valor base, 
    #extra_latitud: rango AÑADIDO a <latitud>, la suma de ambos valores representa el rango superior de la búsqueda
    #extra_longitud rango AÑADIDO a <longitud>, la suma de ambos valores representa el rango superior de la búsqueda
    #menos_latitud: rango RESTADO a <latitud>, la resta de los valores (latitud - menos_latitud) representa el rango inferior de la búsqueda
    #menos_longitud rango RESTADO a <longitud>, la resta de los valores (longitud - menos_longitud) representa el rango inferior de la búsqueda
    #En caso de no idicar alguno de los limites de la base, se indicara 0.003 por defecto.
    def resolve_accesos_cercanos(root, info, longitud, latitud, extra_latitud="0.003", extra_longitud="0.003", menos_latitud="0.003", menos_longitud="0.003", **kwargs):
        try:
            long=Decimal(longitud)
            lat=Decimal(latitud)
            mxlong=long+Decimal(extra_longitud)
            mxlat=lat+Decimal(extra_latitud)
            mnlong=long-Decimal(menos_longitud)
            mnlat=lat-Decimal(menos_latitud)
        except InvalidOperation:
            return ["Error: No se indica un número válido"]
        except Exception as err:
            return ["Error: ocurrió algún problema"]
        return Accesos.objects.filter(longitud__gte=mnlong,latitud__gte=mnlat,longitud__lte=mxlong,latitud__lte=mxlat)

    #Busca todos los accesos y los pagina en resultados
    def resolve_accesos_paginados(root, info, **kwargs):
        return Accesos.objects.all()

    #Busca accesos y los filtra por colonia en caso de que se indique, resultados paginados
    def resolve_ver_colonias(root, info, **kwargs):
        return Accesos.objects.all()

    #En caso de que la petición indique buscar en general, esta funcion filtrará o entregará la lista completa
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
    def resolve_ver_acceso_id(self, info, id):
        id_wifi = id
        try:
            punto = Accesos.objects.filter(id_wifi=id_wifi)
            return punto
        except: return None