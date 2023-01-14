from django.db import models
from django.core.validators import (
    MaxLengthValidator, MinLengthValidator,
)
from datetime import date

class accesos(models.Model):

    id_wifi = models.CharField(
        verbose_name="Identificador:",
        max_length=1000,
        validators=[
            MinLengthValidator(
                0, message="La descripción debe tener por lo menos 1 caracter."),
            MaxLengthValidator(
                1000, message="No puede pasar los 1000 caracteres."),
        ], 
        error_messages={
            "blank": "No puede estar vacío.",
            "required": "No puede estar vacío."
        },
    )

    programa = models.CharField(
        verbose_name="Programa:",
        max_length=1000,
        validators=[
            MinLengthValidator(
                1, message="El programa debe tener por lo menos 1 caracter."),
            MaxLengthValidator(
                1000, message="No puede pasar los 1000 caracteres."),
        ], 
        error_messages={
            "blank": "No puede estar vacío.",
            "required": "No puede estar vacío."
        },
    )

    fecha_instalacion = models.DateField(
        verbose_name="Fecha de instalación",
        default=date.today,
    )

    latitud = models.DecimalField(
        verbose_name="Latitud:",
        max_digits=20, 
        decimal_places=18,
        default = 0,
        error_messages={
            "invalid": "El valor debe ser numérico.",
            "max_digits": "No puedes ingresar más de 8 dígitos en total.",
            "max_decimal_places": "No puedes ingresar más de 6 decimales.",
            "max_whole_digits": "No puedes tener mas de 8 enteros."
        },
    )

    longitud = models.DecimalField(
        verbose_name="Longitud:",
        max_digits=20, 
        decimal_places=18,
        default = 0,
        error_messages={
            "invalid": "El valor debe ser numérico.",
            "max_digits": "No puedes ingresar más de 8 dígitos en total.",
            "max_decimal_places": "No puedes ingresar más de 6 decimales.",
            "max_whole_digits": "No puedes tener mas de 8 enteros."
        },
    )
    
    colonia = models.CharField(
        verbose_name="Colonia:",
        max_length=1000,
        validators=[
            MinLengthValidator(
                1, message="La colonia debe tener por lo menos 1 caracter."),
            MaxLengthValidator(
                1000, message="No puede pasar los 1000 caracteres."),
        ], 
        error_messages={
            "blank": "No puede estar vacío.",
            "required": "No puede estar vacío."
        },
    )

    alcaldia = models.CharField(
        verbose_name="Alcaldía:",
        max_length=1000,
        validators=[
            MinLengthValidator(
                1, message="La alcaldía debe tener por lo menos 1 caracter."),
            MaxLengthValidator(
                1000, message="No puede pasar los 1000 caracteres."),
        ], 
        error_messages={
            "blank": "No puede estar vacío.",
            "required": "No puede estar vacío."
        },
    )