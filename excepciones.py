# excepciones.py
# Errores propios del proyecto.
# Todos heredan de ErrorFlota, así con un solo "except ErrorFlota"
# podemos atrapar cualquiera de ellos.




class ErrorFlota(Exception):
    """Error general del sistema de la flota."""
    pass


class CargaInvalidaError(ErrorFlota):
    """Se lanza cuando los datos de una carga no tienen sentido
    (peso negativo, descripción vacía, nivel fuera de rango, etc.)."""
    pass
