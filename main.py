#Programa principal

from cargas import Carga, Documento, Alimento, Fragil, MaterialLaboratorio
from excepciones import CargaInvalidaError


# Prueba de cargas

def probar_cargas():
    print("=== Avance 1: tipos de carga ===")

    cargas = [
        Documento("Actas del consejo de facultad", 0.8, confidencial=True),
        Documento("Guías de laboratorio", 1.5),
        Alimento("Almuerzo ejecutivo", 2.0, temp_objetivo_c=60),
        Fragil("Microscopio portátil", 6.0, nivel_fragilidad=3),
        MaterialLaboratorio("Ácido clorhídrico 100 ml", 0.5, nivel_peligro=2,
                            codigo_autorizacion="LAB-17"),
    ]

    # (Polimorfismo) hacemos las mismas preguntas a todas
    # y cada tipo de carga responde a su manera
    for c in cargas:
        print(c)
        print("   factor de costo:", c.factor_costo())
        print("   puede ir en dron:", c.admite_dron())
        print("   tolera vibración:", c.tolera_vibracion())
        print("   límite de tiempo (min):", c.tiempo_limite_min())

    print()
    print("=== Avance 1: validaciones ===")

    # 1. Peso negativo
    try:
        Documento("Carta", -2)
    except CargaInvalidaError as e:
        print("Error atrapado (peso):", e)

    # 2. Un documento no puede pesar mucho
    try:
        Documento("Resma de papel", 12)
    except CargaInvalidaError as e:
        print("Error atrapado (límite del tipo):", e)

    # 3. Material de laboratorio sin autorización
    try:
        MaterialLaboratorio("Éter", 1, nivel_peligro=3, codigo_autorizacion="  ")
    except CargaInvalidaError as e:
        print("Error atrapado (autorización):", e)

    # 4. Cambiar el peso después de crear la carga también se valida
    paquete = Fragil("Cámara", 2)
    try:
        paquete.peso_kg = 0
    except CargaInvalidaError as e:
        print("Error atrapado (setter):", e)

    # 5. Carga es abstracta, no se puede crear directamente
    try:
        Carga("algo", 1)
    except TypeError as e:
        print("Error atrapado (clase abstracta):", e)


if __name__ == "__main__":
    probar_cargas()
