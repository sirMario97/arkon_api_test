<p align="center">
  <img width="500" height="140" alt="arkon_data" src="https://user-images.githubusercontent.com/50216075/214129578-a391878e-0e40-4573-95d2-deabdaa95731.svg">
</p>

# Arkon data api
![Badge en Desarollo](https://img.shields.io/badge/Status-En%20desarrollo-green)
![Badge coverage](https://img.shields.io/badge/Coverage-100%20percent-green)
![Badge Python](https://img.shields.io/badge/Language-Python%203.10.7-black)
![Badge graphql](https://img.shields.io/badge/API-GraphQL-black)

Esta es una aplicación pequeña que otorga un entorno, así como un API capás de entregar información perteneciente a los datos abiertos proporcinados por la Ciudad de México. En este 'dataset' se listan todos los puntos de [acceso wiffi](https://datos.cdmx.gob.mx/dataset/puntos-de-acceso-wifi-en-la-ciudad-de-mexico) repartidos por la ciudad.

## API 
Las funcionalidades principales de la api son la entrega de información almacenada en la base de datos usando sentencias unsado la sintaxis de GraphQL. Algunos ejemplos de información la cual puede entregar la aplicación son:

 <ol>
  <li>Una lista paginada de puntos de acceso WiFi</li>
  <li>Información de un punto dado su ID</li>
  <li>Una lista paginada de puntos de acceso dada una colonia</li>
  <li>Una lista paginada de puntos WiFi ordenada por proximidad a unacoordenada dada al indicar la latitud y la longitud</li>
</ol> 
<p align="center">
  <img width="950" height="600" alt="arkon diagrama" src="https://raw.githubusercontent.com/sirMario97/arkon_api_test/main/Arkon%20api.png">
</p>
## Instalación
<em>*Es importante considerar que el desarrollo se realizó sobre el SO de windows, por lo cual, algunas librerías que a continuación se requieren para funcionar, pueden cambiar*</em>

Para poder probar el código habrá que realizar una serie de pasos:

1.- Descarga el proyecto, que refiere a descargar este repositorio:
```sh
#clonando el repositorio de github
git clone https://github.com/sirMario97/arkon_api_test.git
```

2.- Habrá que crear tu entorno virtual venv, utilizando preferiblemente python 3.10.7 y la versión más actual de 'pip':

```sh
#ver la versión de python
python

#actualizar librerias de pip
pip install --upgrade setuptools

#para instalar venv
pip install virtualenv

#Crear el entorno virtual
python -m venv c:\ruta\a_la_carpeta\[proyecto]
```

3.- Una vez creado el entorno virtual, lo iniciamos:
```sh
#Ingresamos a la carpeta del proyecto 'arkon_api'
cd c:\ruta\a_la_carpeta\..\arkon_api_test\arkon_api

#Iniciar el entorno virtual en windows
c:\ruta\a_la_carpeta\[nombre_carpeta_venv]\Scripts\activate
```

4.- Al iniciar el entorno, habrá que instalar la paquetería de desarrolador de [mysql](https://dev.mysql.com/downloads/installer/).

5.- Habrá que instalar las librerías usadas por el API:
```sh
#dentro de la carpeta del proyecto, en '../arkon_api_test/arkon_api/'

pip install -r requirements.txt
```

6.- Si la instalación fue correcta, en mysql creamos un 'schema' o 'database' con el nombre de 'accesos_wifi' allí se crea un usuario para controlar la base de datos. También se le otorgan permisos para crear más bases de datos, ya que este se utilizará por las pruebas unitaraias al crear una base de datos usada para test:
```sh
#iniciamos mysql:
mysql -u root -p

#creamos la base de datos
create database accesos_wifi;

#creamos el usuario y le otorgamos los permisos, respetando el nombre indicado 
#en la sentencia y el indicado en settings.py de django
# ya que estos deben ser iguales (user y psw)
CREATE USER 'arkon_test'@'localhost' IDENTIFIED BY 'arkon_test';
GRANT ALL PRIVILEGES ON * . * TO 'arkon_test'@'localhost';
FLUSH PRIVILEGES;
```

7.-Si no hubo problemas, realizamos las primeras migraciones para que Django cree las tablas dentro de las bases de datos (*no tendrá ningún dato todavía, por lo cual las consultas no regresarán nada*)
```sh
#sin salirnos del entorno virtual, generamos las migraciones:
python manage.py makemigrations
python manage.py migrate

#iniciamos django
python manage.py runserver

#entramos a la siguiente página para comprobar que django funciona:
http://localhost:8000/graphql

#('Ctrl + c' para terminar el proceso en la terminal)
```

8.- Ahora debemos llenar la tabla de puntos_wifi dentro de la base de datos de accesos_wifi:
```sh
#ejecutamos la siguiente sentencia para insertar los datos en la tabla correcta:
mysql -u root -p accesos_wifi <puntos_wifi_accesos.sql>
```

## <p align="left">Busquedas usando akron_api <img width="35" height="35" alt="graphql" src="https://graphql.org/img/logo.svg"><img width="35" height="35" alt="graphene" src="https://camo.githubusercontent.com/eb4acaf18fa97e266aa31536649bee53d1933689a75d6bd9dc0d89eaee96e951/687474703a2f2f6772617068656e652d707974686f6e2e6f72672f66617669636f6e2e706e67"></p>

![Badge graphene](https://img.shields.io/badge/GraphQL-django_graphene-green)

Tras los puntos anteriores podremos, ahora si, realizar consultas siguiendo el lenguaje graphql, por ejemplo:
```sh
#iniciamos django (en caso de haber terminado el proceso)
python manage.py runserver

#entramos nuevamente al sistema usando el navegador con la liga:
http://localhost:8000/graphql

#Sentencia para mostrar la lista total de puntos wifi sin paginar, los parámetros son opcionales:
{
  accesos{
    idWifi
    colonia
    alcaldia
    longitud
    latitud
  }
}

#Sentencia para mostrar la lista total de puntos wifi paginados, los parámetros son opcionales:
{
  accesosPaginados(){
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
        longitud
        latitud
      }
    }
  }
}

#Sentencia para mostrar la lista total de puntos wifi paginados, buscando por una colonia indicada:
{
  verColonias(colonia:"ZONA ESCOLAR ORIENTE"){
     pageInfo{
      startCursor
      endCursor
      hasNextPage
      hasPreviousPage
    }
    edges{
      cursor
      node{
        idWifi
        colonia
        alcaldia
        fechaInstalacion
        longitud
        latitud
      }
    }
  }
}

#Sentencia para mostrar la lista total de puntos wifi, buscando por un id específico:
{
  verAccesoId(id:"Cuautepec"){
    idWifi
    colonia
    alcaldia
    fechaInstalacion
    longitud
    latitud
  }
}

#Sentencia para mostrar la lista total de puntos wifi más cercanos a una coordenada dada:
{
  accesosCercanos(longitud:"-99.142510",latitud:"19.53974"){
    pageInfo{
      hasNextPage
    }
    edges{
      node{
        idWifi
        colonia
        longitud
        latitud
      }
    }
  }
}

#Sentencia para mostrar la lista total de puntos wifi dentro de un rango de coordenadas:
{
  accesosCercanos(longitud:"-99.14251",latitud:"19.53974",extraLatitud:"1",extraLongitud:"1",menosLatitud:"1",menosLongitud:"1"){
    pageInfo{
      hasNextPage
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
```

## Pruebas unitarias
![Badge coverage](https://img.shields.io/badge/Coverage-100%20percent-green)

Traas la instalación de requeriments.txt se añadirá la librería de pytest-django la cual permite realizar pruebas unitarias. Para ejecutarlas, solo será necesario estar dentro del entorno virutal y:
```sh
#ejecutar las pruebas unitarias (unit tests)
pytest
```
Estas pruebas se encuentras desplegadas dentro de la carpeta 'arkon_api_test/arkon_api/tests', donde podrás encontrar las pruebas que utilizan las funcionalidades proporcionadas por el API.

## Docker
![Badge en Desarollo](https://img.shields.io/badge/Status-No%20finalizado-yellow)

La dockerización queda pendiente de terminación. Es una herramienta de despliegue que aun no se domina en un cien porciento, por lo cual no se logró finalizar con la creación correcta de la imagen. Aún así los archivos se adjuntan para su posterior trabajo e implementación total la cual comprendería la imagen correcta de Djnago-mysql así como su contenedor.
