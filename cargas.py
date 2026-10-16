

from abc import ABC, abstractmethod
from excepciones import CargaInvalidaError




class Carga(ABC):
    """Clase base. No se puede crear una Carga "a secas",
    siempre tiene que ser de un tipo concreto."""

    # Cada tipo de carga cambia la variable con su propio límite de peso
    PESO_MAXIMO_KG = 50

    def __init__(self, descripcion, peso_kg):
        # Se usan las propiedades de abajo para que las validaciones
        # se ejecuten desde que se crea el objeto
        self.descripcion = descripcion
        self.peso_kg = peso_kg

    # propiedades 
    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise CargaInvalidaError("La carga necesita una descripción")
        self._descripcion = valor.strip()

    @property
    def peso_kg(self):
        return self._peso_kg

    @peso_kg.setter
    def peso_kg(self, valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise CargaInvalidaError("El peso debe ser un número")
        if valor <= 0:
            raise CargaInvalidaError("El peso debe ser mayor que 0")
        if valor > self.PESO_MAXIMO_KG:
            raise CargaInvalidaError(
                f"{type(self).__name__} no puede pesar más de "
                f"{self.PESO_MAXIMO_KG} kg (se intentó {valor} kg)"
            )
        self._peso_kg = valor

    # métodos 
    @abstractmethod
    def factor_costo(self):
        """Multiplicador del costo base de la entrega (1.0 = normal)."""

    @abstractmethod
    def admite_dron(self):
        """True si esta carga puede viajar por el aire."""

    # ----- métodos con valor por defecto (algunos tipos lo cambian) -----
    def tolera_vibracion(self):
        return True

    def tiempo_limite_min(self):
        # None significa que no hay límite de tiempo
        return None

    def __str__(self):
        return f"{type(self).__name__}: {self._descripcion} ({self._peso_kg} kg)"


class Documento(Carga):
    PESO_MAXIMO_KG = 5

    def __init__(self, descripcion, peso_kg, confidencial=False):
        super().__init__(descripcion, peso_kg)
        self._confidencial = bool(confidencial)

    @property
    def confidencial(self):
        return self._confidencial

    def factor_costo(self):
        # lo confidencial cuesta un poco más
        if self._confidencial:
            return 1.2
        return 1.0

    def admite_dron(self):
        # un dron se puede perder, así que
        # no le damos documentos confidenciales
        return not self._confidencial


class Alimento(Carga):
    PESO_MAXIMO_KG = 15

    def __init__(self, descripcion, peso_kg, temp_objetivo_c, minutos_limite=30):
        super().__init__(descripcion, peso_kg)
        try:
            self._temp_objetivo_c = float(temp_objetivo_c)
            self._minutos_limite = int(minutos_limite)
        except (TypeError, ValueError):
            raise CargaInvalidaError("Temperatura y minutos límite deben ser números")
        if self._minutos_limite <= 0:
            raise CargaInvalidaError("Los minutos límite deben ser mayores que 0")

    @property
    def temp_objetivo_c(self):
        return self._temp_objetivo_c

    def factor_costo(self):
        # Lleva control de temperatura, por eso cuesta más
        return 1.25

    def admite_dron(self):
        return True

    def tiempo_limite_min(self):
        # La comida no puede demorarse mas de  cantidad de minutos
        return self._minutos_limite


class Fragil(Carga):
    PESO_MAXIMO_KG = 20

    def __init__(self, descripcion, peso_kg, nivel_fragilidad=2):
        super().__init__(descripcion, peso_kg)
        if nivel_fragilidad not in (1, 2, 3):
            raise CargaInvalidaError("El nivel de fragilidad va de 1 a 3")
        self._nivel_fragilidad = nivel_fragilidad

    @property
    def nivel_fragilidad(self):
        return self._nivel_fragilidad

    def factor_costo(self):
        # Entre más frágil, más cuidado y más cuesta
        return 1.2 + 0.1 * self._nivel_fragilidad

    def admite_dron(self):
        # Lo muy frágil no se puede arriesga con el viento del dron
        return self._nivel_fragilidad <= 2

    def tolera_vibracion(self):
        return False


class MaterialLaboratorio(Carga):
    PESO_MAXIMO_KG = 10

    def __init__(self, descripcion, peso_kg, nivel_peligro, codigo_autorizacion):
        super().__init__(descripcion, peso_kg)
        if nivel_peligro not in (1, 2, 3):
            raise CargaInvalidaError("El nivel de peligro va de 1 a 3")
        if not isinstance(codigo_autorizacion, str) or codigo_autorizacion.strip() == "":
            raise CargaInvalidaError("El material de laboratorio necesita código de autorización")
        self._nivel_peligro = nivel_peligro
        self._codigo_autorizacion = codigo_autorizacion.strip()

    @property
    def nivel_peligro(self):
        return self._nivel_peligro

    @property
    def codigo_autorizacion(self):
        return self._codigo_autorizacion

    def factor_costo(self):
        return 1.5 + 0.25 * self._nivel_peligro

    def admite_dron(self):
        # Nunca por aire
        return False

    def tolera_vibracion(self):
        return False
