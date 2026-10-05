"""
=============================================================================
TECNOLÓGICO NACIONAL DE MÉXICO - INSTITUTO TECNOLÓGICO SUPERIOR DE URUAPAN
DIVISIÓN DE ESTUDIOS DE POSGRADO E INVESTIGACIÓN
MAESTRÍA EN INTELIGENCIA ARTIFICIAL

Materia: Inteligencia Artificial y su Ética
Actividad 26: Proyecto "Diseña tu Primer Robot Virtual"
Contexto: Startup de robótica de servicio doméstico.
Alumno: Juan Pablo Figueroa Moran (Matrícula: M26040059)
=============================================================================
"""

import sys
import heapq
import time
from typing import List, Tuple, Set, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# =============================================================================
# CLASE BASE DE ROBOT AUTÓNOMO
# =============================================================================

class RobotAutonomo:
    """Clase base de plataforma robótica móvil con sensores de navegación."""
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.posicion = (0, 0)
        self.obstaculos = set()

    def navegar_a_destino(self, x: int, y: int) -> bool:
        """Verifica si la celda es transitable (no es obstáculo)."""
        if (x, y) in self.obstaculos:
            return False
        self.posicion = (x, y)
        return True


# =============================================================================
# ALGORITMO A* PARA NAVEGACIÓN Y RETORNO ÓPTIMO A BASE
# =============================================================================

def planificar_retorno_a_estrella(inicio: Tuple[int, int], meta: Tuple[int, int],
                                  obstaculos: Set[Tuple[int, int]],
                                  ancho: int, alto: int) -> List[Tuple[int, int]]:
    """Encuentra la ruta mínima libre de obstáculos usando A*."""
    def h(p):
        return abs(p[0] - meta[0]) + abs(p[1] - meta[1])

    open_set = []
    heapq.heappush(open_set, (h(inicio), 0, inicio, [inicio]))
    visitados = set()

    while open_set:
        f, g, actual, camino = heapq.heappop(open_set)
        if actual == meta:
            return camino
        if actual in visitados:
            continue
        visitados.add(actual)

        x, y = actual
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ancho and 0 <= ny < alto:
                if (nx, ny) not in obstaculos and (nx, ny) not in visitados:
                    heapq.heappush(open_set, (g + 1 + h((nx, ny)), g + 1, (nx, ny), camino + [(nx, ny)]))

    return []


# =============================================================================
# PLANTILLA REQUERIDA DEL ENUNCIADO: ROBOT LIMPIADOR AUTÓNOMO
# =============================================================================

def proyecto_robot_limpiador():
    """Plantilla requerida para el proyecto del robot limpiador."""
    print("=" * 80)
    print(" Proyecto: Robot Limpiador Autónomo")
    print("=" * 80)

    class RobotLimpiador(RobotAutonomo):
        def __init__(self, nombre: str, ancho: int = 7, alto: int = 7):
            super().__init__(nombre)
            self.ancho = ancho
            self.alto = alto
            self.areas_limpias = set()
            self.bateria = 100
            self.capacidad_basura = 100
            self.base = (0, 0)
            self.ciclos_recarga = 0
            self.pasos_totales = 0

            # Obstáculos domésticos (muebles, paredes intermedias)
            self.obstaculos = {(2, 1), (2, 2), (2, 3), (4, 5), (5, 5)}

        def limpiar_area(self, x: int, y: int) -> bool:
            """Simula limpiar un área específica."""
            if (x, y) in self.areas_limpias:
                return False

            if self.bateria <= 0:
                print(" Batería agotada, no se puede limpiar")
                return False

            self.bateria -= 1
            self.capacidad_basura -= 1
            self.areas_limpias.add((x, y))
            return True

        def recargar_en_base(self):
            """Simula el retorno guiado por A*, recarga de batería y vaciado de depósito."""
            ruta_retorno = planificar_retorno_a_estrella(self.posicion, self.base, self.obstaculos, self.ancho, self.alto)
            print(f"[*] Planificando ruta de evacuación hacia la base {self.base} con A*...")
            print(f"    Ruta encontrada ({len(ruta_retorno)} pasos): {ruta_retorno}")
            self.posicion = self.base
            self.ciclos_recarga += 1
            self.bateria = 100
            self.capacidad_basura = 100
            print(f"[+] Robot seguro en Base {self.base}. Depósito vaciado y batería recargada al 100%.\n")

        def planificar_ruta_limpieza(self, ancho: int, alto: int):
            """Planifica una ruta sistemática Boustrophedon optimizada con retorno A*."""
            print(f"\n Planificando ruta de limpieza para área {ancho}x{alto}")
            areas_por_limpiar = ancho * alto - len(self.obstaculos)
            areas_limpiadas = 0

            # Barrido en serpiente (Boustrophedon)
            for y in range(alto):
                rango_x = range(ancho) if y % 2 == 0 else range(ancho - 1, -1, -1)
                for x in rango_x:
                    if (x, y) in self.obstaculos:
                        continue

                    if self.navegar_a_destino(x, y):
                        self.pasos_totales += 1
                        if self.limpiar_area(x, y):
                            areas_limpiadas += 1

                    # Monitoreo de seguridad energética
                    if self.bateria <= 20:
                        print(f"\n[⚠️ ALERTA CRÍTICA] Batería al {self.bateria}% (<= 20%). Interrumpiendo misión.")
                        self.recargar_en_base()

            return areas_limpiadas

        def mostrar_mapa(self):
            """Renderiza el mapa en formato ASCII."""
            print("\n--- Visualización de la Cuadrícula del Hogar ---")
            for y in range(self.alto):
                fila = []
                for x in range(self.ancho):
                    if (x, y) == self.posicion:
                        fila.append("R")
                    elif (x, y) == self.base:
                        fila.append("B")
                    elif (x, y) in self.obstaculos:
                        fila.append("#")
                    elif (x, y) in self.areas_limpias:
                        fila.append(".")
                    else:
                        fila.append("S")
                print("  " + " ".join(fila))
            print("  Leyenda: B=Base, R=Robot, .=Limpia, S=Sucia, #=Obstáculo\n")

    print("\n Tu tarea: Completa la clase RobotLimpiador y optimiza su comportamiento")
    return RobotLimpiador


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

def main():
    RobotLimpiadorClass = proyecto_robot_limpiador()

    robot = RobotLimpiadorClass(nombre="CleanBot-v2", ancho=7, alto=7)
    # Batería inicial para forzar ciclo de recarga pedagógico
    robot.bateria = 45

    print("Estado inicial del entorno:")
    robot.mostrar_mapa()

    # Ejecutar cobertura y navegación
    total_limpias = robot.planificar_ruta_limpieza(robot.ancho, robot.alto)

    print("=" * 75)
    print("  REPORTE FINAL DE LA MISIÓN DEL ROBOT LIMPIADOR DOMÉSTICO")
    print("=" * 75)
    print(f"  * Celdas limpiadas: {total_limpias} de {robot.ancho * robot.alto - len(robot.obstaculos)} transitables (100% cobertura)")
    print(f"  * Pasos totales realizados: {robot.pasos_totales}")
    print(f"  * Ciclos de recarga en base: {robot.ciclos_recarga}")
    print(f"  * Nivel final de batería: {robot.bateria}%")

    print("\nEstado final del entorno:")
    robot.mostrar_mapa()

    # Consideraciones Éticas
    print("=" * 75)
    print("  CONSIDERACIONES ÉTICAS EN ROBÓTICA DOMÉSTICA")
    print("=" * 75)
    print("  1. Seguridad Física y Personas Vulnerables: El robot debe detenerse de forma")
    print("     inmediata ante la presencia de niños, mascotas o ancianos en su campo de visión.")
    print("  2. Privacidad de Mapas Espaciales: Los planos topográficos del hogar deben")
    print("     mantenerse cifrados localmente, prohibiendo su telemetría hacia la nube sin permiso.")
    print("  3. Eficiencia Energética: El algoritmo A* optimiza el retorno reduciendo el")
    print("     desgaste de los ciclos de carga de la batería de litio.")
    print("=" * 75)


if __name__ == "__main__":
    main()
