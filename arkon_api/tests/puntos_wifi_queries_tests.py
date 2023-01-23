from django.db import models
import pytest
import datetime
from pytest import raises
import graphene
from puntos_wifi.models import Accesos
from puntos_wifi.schema import Query as Qry

from decimal import Decimal

@pytest.mark.django_db
def test_query_solo_fields():
    with raises(Exception):
        class AccesoType(DjangoObjectType):
            class Meta:
                model = Accesos
                fields = ("id_wifi",)
        schema = graphene.Schema(query=AccesoType)
        query = """
            query AccesosQuery {
                id_wifi
            }
        """
        result = schema.execute(query)
        assert not result.errors

"""
Funcion que inserta los registros en la DB de prueba
"""
def inserta_accesos():
    accesos = [
        Accesos.objects.create(
            id_wifi="Cuautepec",
            programa="Sitios Publicos",
            fecha_instalacion=datetime.date(2018,12,15),
            longitud=Decimal(-99.142510000000000000),
            latitud=Decimal(19.539740000000000000),
            colonia="ZONA ESCOLAR ORIENTE",
            alcaldia="GUSTAVO A. MADERO",
        ),
        Accesos.objects.create(
            id_wifi="Moctezuma",
            programa="Sitios Publicos",
            fecha_instalacion=datetime.date(2018,12,15),
            longitud=Decimal(-99.098010000000000000),
            latitud=Decimal(19.432630000000000000),
            colonia="MOCTEZUMA 2A SECCION II",
            alcaldia="VENUSTIANO CARRANZA",
        ),
        Accesos.objects.create(
            id_wifi="San Juan De Aragón",
            programa="Sitios Publicos",
            fecha_instalacion=datetime.date(2018,12,15),
            longitud=Decimal(-99.093140000000000000),
            latitud=Decimal(19.457190000000000000),
            colonia="SAN JUAN DE ARAGON 1A SECCION (U HAB) I",
            alcaldia="GUSTAVO A. MADERO",
        ),
        Accesos.objects.create(
            id_wifi="Cuautepec",
            programa="Sitios Publicos",
            fecha_instalacion=datetime.date(2018,12,15),
            longitud=Decimal(-99.142510000000000000),
            latitud=Decimal(19.539740000000000000),
            colonia="ZONA ESCOLAR ORIENTE",
            alcaldia="GUSTAVO A. MADERO",
        ),
    ]

"""
Prueba para corroborar el funcionamiento de una lista de puntos sin paginar
-creamos algunos datos
-se ejecuta petición
-se corroboran resultados
"""
@pytest.mark.django_db
def test_query_muestra_lista_puntos():
    schema = graphene.Schema(query=Qry)#Referenciamos a los queries creados en el modelo de puntos_wifi
    #creamos unos registros en la BD de prueba
    inserta_accesos()
    #creamos la petición
    query="""
        {
            accesos{
                idWifi
            }
        }
    """
    #indicamos lo que esperamos obtener en la petición
    q_expected = {
        "accesos":[ 
            {"idWifi": "Cuautepec"},
            {"idWifi": "Moctezuma"},
            {"idWifi": "San Juan De Aragón"},
            {"idWifi": "Cuautepec"},
        ],
    }

    result = schema.execute(query)#ejecutamos la petición
    assert not result.errors#verificamos que no haya errores
    assert result.data == q_expected#verificamos el resultado contra lo esperado

"""
Prueba para corroborar el funcionamiento de una lista de puntos PAGINADA
-creamos algunos datos
-se ejecuta petición
-se corroboran resultados
"""
@pytest.mark.django_db
def test_query_resolve_accesos_paginados():
    schema = graphene.Schema(query=Qry)#Referenciamos a los queries creados en el modelo de puntos_wifi
    #creamos unos registros en la BD de prueba
    inserta_accesos()
    #creamos la petición
    query="""
    {
        accesosPaginados(first:2,){
            pageInfo{
            hasNextPage
            hasPreviousPage
            }
            edges{
            node{
                idWifi
                colonia
                alcaldia
                fechaInstalacion
            }
            }
        }
    }
    """
    #indicamos lo que esperamos obtener en la petición
    q_expected = {
        "accesosPaginados": {
            "pageInfo": {
                "hasNextPage": True,
                "hasPreviousPage": False
            },
            "edges": [
                {
                    "node": {
                        "idWifi": "Cuautepec",
                        "colonia": "ZONA ESCOLAR ORIENTE",
                        "alcaldia": "GUSTAVO A. MADERO",
                        "fechaInstalacion": "2018-12-15",
                    }
                },
                {
                    "node": {
                        "idWifi": "Moctezuma",
                        "colonia": "MOCTEZUMA 2A SECCION II",
                        "alcaldia": "VENUSTIANO CARRANZA",
                        "fechaInstalacion": "2018-12-15",
                    }
                }
            ]
        }
    }
    result = schema.execute(query)#ejecutamos la petición
    assert not result.errors#verificamos que no haya errores
    assert result.data["accesosPaginados"]["edges"] == q_expected["accesosPaginados"]["edges"]#verificamos el resultado de los nodos (púntos wifi)
    assert result.data["accesosPaginados"]["pageInfo"] == q_expected["accesosPaginados"]["pageInfo"]#verificamos el resultado de las páginas

"""
Prueba para corroborar el funcionamiento de una lista de puntos wifi, dado un id
-creamos algunos datos
-se ejecuta petición
-se corroboran resultados
"""
@pytest.mark.django_db
def test_query_resolve_ver_acceso_id():
    schema = graphene.Schema(query=Qry)#Referenciamos a los queries creados en el modelo de puntos_wifi
    inserta_accesos()
    #creamos la petición
    query="""
    {
        verColonias(first:2,idWifi:"Cuautepec"){
            pageInfo{
                hasNextPage
                hasPreviousPage
            }
            edges{
                node{
                    idWifi
                    colonia
                }
            }
        }
    }
    """
    #indicamos lo que esperamos obtener en la petición
    q_expected = {
        "verColonias": {
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False
            },
            "edges": [
                {
                    "node": {
                        "idWifi": "Cuautepec",
                        "colonia": "ZONA ESCOLAR ORIENTE",
                    }
                },
                {
                    "node": {
                        "idWifi": "Cuautepec",
                        "colonia": "ZONA ESCOLAR ORIENTE",
                    }
                }
            ]
        }
    }
    result = schema.execute(query)#ejecutamos la petición
    assert not result.errors#verificamos que no haya errores
    assert result.data["verColonias"]["edges"] == q_expected["verColonias"]["edges"]#verificamos el resultado de los nodos (púntos wifi)
    assert result.data["verColonias"]["pageInfo"] == q_expected["verColonias"]["pageInfo"]#verificamos el resultado de las páginas

"""
Prueba para corroborar el funcionamiento de una lista de puntos wifi buscando por la 'colonia'
-creamos algunos datos
-se ejecuta petición
-se corroboran resultados
"""
@pytest.mark.django_db
def test_query_resolve_ver_colonias():
    schema = graphene.Schema(query=Qry)#Referenciamos a los queries creados en el modelo de puntos_wifi
    #creamos unos registros en la BD de prueba
    inserta_accesos()
    #creamos la petición
    query="""
    {
        verColonias(first:3,colonia:"ZONA ESCOLAR ORIENTE"){
            pageInfo{
                hasNextPage
                hasPreviousPage
            }
            edges{
                node{
                    idWifi
                    colonia
                }
            }
        }
    }
    """
    #indicamos lo que esperamos obtener en la petición
    q_expected = {
        "verColonias": {
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False
            },
            "edges": [
                {
                    "node": {
                        "idWifi": "Cuautepec",
                        "colonia": "ZONA ESCOLAR ORIENTE",
                    }
                },
                {
                    "node": {
                        "idWifi": "Cuautepec",
                        "colonia": "ZONA ESCOLAR ORIENTE",
                    }
                }
            ]
        }
    }
    result = schema.execute(query)#ejecutamos la petición
    assert not result.errors#verificamos que no haya errores
    assert result.data["verColonias"]["edges"] == q_expected["verColonias"]["edges"]#verificamos el resultado de los nodos (púntos wifi)
    assert result.data["verColonias"]["pageInfo"] == q_expected["verColonias"]["pageInfo"]#verificamos el resultado de las páginas

"""
Prueba para corroborar el funcionamiento de una lista de puntos wifi más cercanos a una cordenada
-creamos algunos datos
-se ejecuta petición
-se corroboran resultados
"""
@pytest.mark.django_db
def test_query_resolve_accesos_cercanos():
    schema = graphene.Schema(query=Qry)#Referenciamos a los queries creados en el modelo de puntos_wifi
    inserta_accesos()
    #creamos la petición
    query="""
    {
        accesosCercanos(longitud:"-99.14251",latitud:"19.53974"){
            pageInfo{
                hasNextPage
                hasPreviousPage
            }
            edges{
                node{
                    idWifi
                    alcaldia
                    colonia
                }
            }
        }
    }
    """
    #indicamos lo que esperamos obtener en la petición
    q_expected = {
        "accesosCercanos": {
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False
            },
            "edges": [
                {
                    "node": {
                        "idWifi": "Cuautepec",
                        "alcaldia": "GUSTAVO A. MADERO",
                        "colonia": "ZONA ESCOLAR ORIENTE",
                    }
                },
                {
                    "node": {
                        "idWifi": "Cuautepec",
                        "alcaldia": "GUSTAVO A. MADERO",
                        "colonia": "ZONA ESCOLAR ORIENTE",
                    }
                }
            ]
        }
    }
    result = schema.execute(query)#ejecutamos la petición
    assert not result.errors#verificamos que no haya errores
    assert result.data["accesosCercanos"]["edges"] == q_expected["accesosCercanos"]["edges"]#verificamos el resultado de los nodos (púntos wifi)
    assert result.data["accesosCercanos"]["pageInfo"] == q_expected["accesosCercanos"]["pageInfo"]#verificamos el resultado de las páginas


"""
Prueba para corroborar el funcionamiento de una lista de puntos wifi más cercanos a un rango de cordenadas
-creamos algunos datos
-se ejecuta petición
-se corroboran resultados
"""
@pytest.mark.django_db
def test_query_resolve_accesos_cercanos_rango():
    schema = graphene.Schema(query=Qry)#Referenciamos a los queries creados en el modelo de puntos_wifi
    #creamos unos registros en la BD de prueba
    inserta_accesos()
    #creamos la petición, pero ahora tendrá cuatro atributuos que establecen un rango abuscar
    query="""
    {
        accesosCercanos(longitud:"-99.14251",latitud:"19.53974",extraLatitud:"1",extraLongitud:"1",menosLatitud:"1",menosLongitud:"1"){
            pageInfo{
                hasNextPage
                hasPreviousPage
            }
            edges{
                node{
                    idWifi
                    alcaldia
                    colonia
                }
            }
        }
    }
    """
    #indicamos lo que esperamos obtener en la petición
    q_expected = {
        "accesosCercanos": {
            "pageInfo": {
                "hasNextPage": False,
                "hasPreviousPage": False
            },
            "edges": [
                {
                    "node": {
                        "idWifi": "Cuautepec",
                        "alcaldia": "GUSTAVO A. MADERO",
                        "colonia": "ZONA ESCOLAR ORIENTE",
                    }
                },
                {
                    "node": {
                        "idWifi": "Moctezuma",
                        "alcaldia": "VENUSTIANO CARRANZA",
                        "colonia": "MOCTEZUMA 2A SECCION II",
                    }
                },
                {
                    "node": {
                        "idWifi": "San Juan De Aragón",
                        "alcaldia": "GUSTAVO A. MADERO",
                        "colonia": "SAN JUAN DE ARAGON 1A SECCION (U HAB) I",
                    }
                },
                {
                    "node": {
                        "idWifi": "Cuautepec",
                        "alcaldia": "GUSTAVO A. MADERO",
                        "colonia": "ZONA ESCOLAR ORIENTE",
                    }
                }
            ]
        }
    }
    result = schema.execute(query)#ejecutamos la petición
    assert not result.errors#verificamos que no haya errores
    assert result.data["accesosCercanos"]["edges"] == q_expected["accesosCercanos"]["edges"]#verificamos el resultado de los nodos (púntos wifi)
    assert result.data["accesosCercanos"]["pageInfo"] == q_expected["accesosCercanos"]["pageInfo"]#verificamos el resultado de las páginas
