from colorama import init, Fore, Back, Style
from clases import Detector, Radiacion, Virus, Sanador

def ingresar_matriz() -> list[str]:
    """
    Permite al usuario ingresar una matriz de ADN de 6x6.

    :return: Lista de cadenas que representan la matriz de ADN.
    """
    print (Fore.CYAN + "Ingrese las filas de la matriz de ADN (6 cadenas de 6 caracteres, usando A, T, C, G):")
    matriz = []
    for i in range(6):
        while True:
            fila = input(f"Fila {i + 1}: ").strip().upper()
            if len(fila) == 6 and all(base in "ATCG" for base in fila):
                matriz.append(fila)
                break
            else:
                print("\nError: La fila debe tener exactamente 6 caracteres y solo contener A, T, C o G.")
    return matriz


def mostrar_matriz(matriz: list[str]) -> None:
    """
    Muestra una matriz de ADN de forma legible.

    :param matriz: Lista de cadenas que representan la matriz de ADN.
    """
    print("\nMatriz de ADN actual:")
    for fila in matriz:
        print(" ".join(fila))


def main():
    print(Style.BRIGHT + Fore.CYAN +"\nBienvenido al programa de análisis de ADN")

    matriz = ingresar_matriz()

    while True:
        print(Fore.RED +"\nMenú:")
        print(Fore.LIGHTYELLOW_EX +"1. Detectar mutaciones")
        print(Fore.LIGHTYELLOW_EX +"2. Crear mutación")
        print(Fore.LIGHTYELLOW_EX +"3. Sanar ADN")
        print(Fore.RED +"4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Detectar mutaciones
            detector = Detector()
            tiene_mutaciones = detector.detectar_mutantes(matriz)
            print(Fore.GREEN + "\n¿El ADN tiene mutaciones?", "Sí" if tiene_mutaciones else "No")
        elif opcion == "2":
            # Crear mutación
            while True:
                print("\nCreación de mutaciones:")
                print("1. Mutación horizontal o vertical (Radiación)")
                print("2. Mutación diagonal (Virus)")
                print("3. Volver")
                sub_opcion = input("Seleccione una opción: ")

                if sub_opcion == "1":
                    base = input("Ingrese la base nitrogenada para la mutación (A, T, C, G): ").strip().upper()
                    if base not in "ATCG":
                        print("\nBase nitrogenada inválida.")
                        continue
                    while True:
                            try:
                                x = int(input("Fila inicial de la mutación (0-5): "))
                                y = int(input("Columna inicial de la mutación (0-5): "))

                                if x < 0 or x > 5 or y < 0 or y > 5:
                                    raise ValueError("Las coordenadas deben estar en el rango de 0 a 5.")
                                
                                break
                            except ValueError as e:
                                print(f"\nError: {e}. Por favor ingrese un número entero válido entre 0 y 5.")
                    while True:
                        orientacion = input("Orientación ('H' para horizontal, 'V' para vertical): ").strip().upper()
                        if orientacion in ['H', 'V']:
                            break
                        else:
                            print("\nError: La orientación debe ser 'H' para horizontal o 'V' para vertical. Intente nuevamente.")
                    radiacion = Radiacion(base)
                    try:
                        matriz = radiacion.crear_mutante(matriz, (x, y), orientacion)
                        print("\nMutación aplicada correctamente.")
                    except ValueError as e:
                        print(f"\nError: {e}")
                    break
                elif sub_opcion == "2":
                    base = input("Ingrese la base nitrogenada para la mutación (A, T, C, G): ").strip().upper()
                    if base not in "ATCG":
                        print("Base nitrogenada inválida.")
                        continue
                    x = int(input("Fila inicial de la mutación diagonal (0-5): "))
                    y = int(input("Columna inicial de la mutación diagonal (0-5): "))
                    virus = Virus(base)
                    try:
                        matriz = virus.crear_mutante(matriz, (x, y))
                        print("\nMutación aplicada correctamente.")
                    except ValueError as e:
                        print(f"Error: {e}")
                    break
                elif sub_opcion == "3":
                    break
                else:
                    print("\nOpción inválida, intente nuevamente.")
                    continue
        elif opcion == "3":
            # Sanar ADN
            sanador = Sanador()
            matriz = sanador.sanar_mutantes(matriz)
            print(Fore.GREEN +"\nEl ADN ha sido sanado.")
        elif opcion == "4":
            print(Fore.GREEN + "\nSaliendo del programa...")
            break
        else:
            print(Fore.GREEN + "\nOpción inválida, intente nuevamente.")

        mostrar_matriz(matriz)


if __name__ == "__main__":
    main()
