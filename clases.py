import random

class Detector:
    """Clase encargada de detectar mutantes en matrices de ADN."""

    def __init__(self, dimensiones: tuple[int, int] = (6, 6)):
        """
        Inicializa un Detector.

        :param dimensiones: Dimensiones de la matriz de ADN (filas, columnas).
        """
        self.dimensiones = dimensiones

    def detectar_mutantes(self, matriz: list[str]) -> bool:
        """
        Detecta si una matriz contiene mutantes en forma horizontal, vertical o diagonal.

        :param matriz: Matriz de ADN representada como una lista de strings.
        :return: True si contiene mutantes, False en caso contrario.
        """
        return any(
            [
                self._check_horizontal(matriz),
                self._check_vertical(matriz),
                self._check_diagonal(matriz),
            ]
        )

    def _check_horizontal(self, matriz: list[str]) -> bool:
        for fila in matriz:
            for i in range(len(fila) - 3):
                if fila[i:i + 4] == fila[i] * 4:
                    return True
        return False

    def _check_vertical(self, matriz: list[str]) -> bool:
        for col in range(len(matriz[0])):
            columna = ''.join(fila[col] for fila in matriz)
            for i in range(len(columna) - 3):
                if columna[i:i + 4] == columna[i] * 4:
                    return True
        return False

    def _check_diagonal(self, matriz: list[str]) -> bool:
        for i in range(len(matriz) - 3):
            for j in range(len(matriz[i]) - 3):
                if all(matriz[i + k][j + k] == matriz[i][j] for k in range(4)) or \
                        all(matriz[i + k][j + 3 - k] == matriz[i][j + 3] for k in range(4)):
                    return True
        return False


class Mutador:
    """Clase base para mutadores de ADN."""

    def __init__(self, base_nitrogenada: str):
        """
        Inicializa un Mutador.

        :param base_nitrogenada: Base nitrogenada que se repetirá en la mutación.
        """
        self.base_nitrogenada = base_nitrogenada

    def crear_mutante(self):
        raise NotImplementedError("Este método debe implementarse en las subclases.")


class Radiacion(Mutador):
    """Clase que representa la radiación y crea mutantes horizontales y verticales."""

    def crear_mutante(
        self,
        matriz: list[str],
        posicion_inicial: tuple[int, int],
        orientacion_de_la_mutacion: str,
    ) -> list[str]:
        """
        Crea una mutación en la matriz.

        :param matriz: Matriz de ADN original.
        :param posicion_inicial: Coordenadas (fila, columna) de la mutación.
        :param orientacion_de_la_mutacion: 'H' para horizontal o 'V' para vertical.
        :return: Matriz con la mutación aplicada.
        """
        try:
            x, y = posicion_inicial
            if orientacion_de_la_mutacion == "H":
                matriz[x] = (
                    matriz[x][:y]
                    + self.base_nitrogenada * 4
                    + matriz[x][y + 4:]
                )
            elif orientacion_de_la_mutacion == "V":
                for i in range(4):
                    matriz[x + i] = (
                        matriz[x + i][:y]
                        + self.base_nitrogenada
                        + matriz[x + i][y + 1:]
                    )
            else:
                raise ValueError("Orientación inválida. Use 'H' o 'V'.")
        except IndexError as e:
            print(f"Error al aplicar mutación: {e}")
        return matriz


class Virus(Mutador):
    """Clase que representa un virus y crea mutantes diagonales."""

    def crear_mutante(
        self, matriz: list[str], posicion_inicial: tuple[int, int]
    ) -> list[str]:
        """
        Crea una mutación diagonal en la matriz.

        :param matriz: Matriz de ADN original.
        :param posicion_inicial: Coordenadas (fila, columna) de la mutación.
        :return: Matriz con la mutación aplicada.
        """
        try:
            x, y = posicion_inicial
            for i in range(4):
                matriz[x + i] = (
                    matriz[x + i][:y + i]
                    + self.base_nitrogenada
                    + matriz[x + i][y + i + 1:]
                )
        except IndexError as e:
            print(f"Error al aplicar mutación diagonal: {e}")
        return matriz


class Sanador:
    """Clase encargada de sanar ADN mutado."""

    def __init__(self):
        """
        Inicializa un Sanador.
        """
        self.detector = Detector()

    def sanar_mutantes(self, matriz: list[str]) -> list[str]:
        """
        Genera una nueva matriz de ADN si se detectan mutantes.

        :param matriz: Matriz de ADN original.
        :return: Nueva matriz de ADN sin mutantes.
        """
        if not self.detector.detectar_mutantes(matriz):
            return matriz

        bases = "ATCG"
        nueva_matriz = [
            ''.join(random.choice(bases) for _ in range(6)) for _ in range(6)
        ]
        while self.detector.detectar_mutantes(nueva_matriz):
            nueva_matriz = [
                ''.join(random.choice(bases) for _ in range(6)) for _ in range(6)
            ]
        return nueva_matriz
