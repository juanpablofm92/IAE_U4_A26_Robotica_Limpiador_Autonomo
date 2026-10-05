"""
=============================================================================
TECNOLÓGICO NACIONAL DE MÉXICO - INSTITUTO TECNOLÓGICO SUPERIOR DE URUAPAN
DIVISIÓN DE ESTUDIOS DE POSGRADO E INVESTIGACIÓN
MAESTRÍA EN INTELIGENCIA ARTIFICIAL

Materia: Inteligencia Artificial y su Ética
Actividad 26: Robótica - Robot Limpiador Autónomo con Boustrophedon y Retorno A*
Alumno: Juan Pablo Figueroa Moran (Matrícula: M26040059)
=============================================================================
"""

import sys
import heapq
import time
from typing import List, Tuple, Optional, Set

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Constantes del Entorno
BASE = (0, 0)
CELDA_LIMPIA = 0
CELDA_SUCIA = 1
CELDA_OBSTACULO = 2


def distancia_manhattan(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def planificar_retorno_a_estrella(cuadricula: List[List[int]], inicio: Tuple[int, int], meta: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Algoritmo de búsqueda A* para encontrar la ruta más corta libre de obstáculos
    desde la posición actual hacia la estación base de recarga.
    """
    filas = len(cuadricula)
    columnas = len(cuadricula[0])

    # Priority queue: (f_score, g_score, (r, c), path)
    open_set = []
    heapq.heappush(open_set, (distancia_manhattan(inicio, meta), 0, inicio, [inicio]))
    visitados = set()

    while open_set:
        f, g, actual, camino = heapq.heappop(open_set)

        if actual == meta:
            return camino

        if actual in visitados:
            continue
        visitados.add(actual)

        r, c = actual
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < filas and 0 <= nc < columnas:
                if cuadricula[nr][nc] != CELDA_OBSTACULO and (nr, nc) not in visitados:
                    nuevo_g = g + 1
                    nuevo_f = nuevo_g + distancia_manhattan((nr, nc), meta)
                    heapq.heappush(open_set, (nuevo_f, nuevo_g, (nr, nc), camino + [(nr, nc)]))

    return [] # Sin ruta viable


class RobotLimpiador:
    """
    Agente robótico autónomo para cobertura de área:
    - Movimiento en patrón de serpiente/escorpión (Boustrophedon)
    - Sensores de detección de proximidad para evasión de obstáculos
    - Monitoreo de batería con retorno seguro A* al caer por debajo del 20%
    """
    def __init__(self, filas: int = 8, columnas: int = 8, bateria_inicial: float = 100.0):
        self.filas = filas
        self.columnas = columnas
        self.posicion = (0, 0)
        self.bateria = bateria_inicial
        self.cuadricula = [[CELDA_SUCIA for _ in range(columnas)] for _ in range(filas)]
        self.celdas_limpiadas = 0
        self.pasos_totales = 0
        self.ciclos_recarga = 0

    def sembrar_obstaculos(self, lista_obstaculos: List[Tuple[int, int]]):
        for r, c in lista_obstaculos:
            if (r, c) != BASE and 0 <= r < self.filas and 0 <= c < self.columnas:
                self.cuadricula[r][c] = CELDA_OBSTACULO

    def ejecutar_ciclo_limpieza(self):
        print(f"[*] Iniciando misión en entorno {self.filas}x{self.columnas}. Batería inicial: {self.bateria}%\n")
        self._limpiar_celda_actual()

        # Cobertura en serpiente (Boustrophedon): fila por fila alternando dirección
        for r in range(self.filas):
            rango_c = range(self.columnas) if r % 2 == 0 else range(self.columnas - 1, -1, -1)
            for c in rango_c:
                meta_celda = (r, c)
                if self.posicion == meta_celda:
                    continue

                # Si es un obstáculo conocido, omitir
                if self.cuadricula[r][c] == CELDA_OBSTACULO:
                    continue

                # Desplazarse hacia la siguiente celda del patrón
                self._mover_hacia(meta_celda)
                self._limpiar_celda_actual()

                # Chequeo crítico de batería (< 20%)
                if self.bateria < 20.0:
                    print(f"\n[⚠️ ALERTA CRÍTICA] Batería al {self.bateria:.1f}% (< 20%). Interrumpiendo misión.")
                    self.retornar_a_base_y_recargar()

        print("\n" + "=" * 70)
        print("  REPORTE FINAL DE LA MISIÓN DEL ROBOT LIMPIADOR")
        print("=" * 70)
        total_limpiables = sum(row.count(CELDA_LIMPIA) for row in self.cuadricula) + sum(row.count(CELDA_SUCIA) for row in self.cuadricula)
        print(f"  * Celdas limpiadas: {self.celdas_limpiadas}")
        print(f"  * Pasos totales realizados: {self.pasos_totales}")
        print(f"  * Ciclos de recarga en base: {self.ciclos_recarga}")
        print(f"  * Nivel final de batería: {self.bateria:.1f}%")
        self.renderizar_mapa()

    def _mover_hacia(self, objetivo: Tuple[int, int]):
        """Intenta avanzar un paso hacia el objetivo evadiendo obstáculos locales."""
        camino = planificar_retorno_a_estrella(self.cuadricula, self.posicion, objetivo)
        if len(camino) > 1:
            for siguiente_paso in camino[1:]:
                self.posicion = siguiente_paso
                self.pasos_totales += 1
                self.bateria -= 0.8  # Consumo por desplazamiento
                if self.bateria < 20.0:
                    break

    def _limpiar_celda_actual(self):
        r, c = self.posicion
        if self.cuadricula[r][c] == CELDA_SUCIA:
            self.cuadricula[r][c] = CELDA_LIMPIA
            self.celdas_limpiadas += 1
            self.bateria -= 1.0  # Consumo extra por succión/cepillado

    def retornar_a_base_y_recargar(self):
        print(f"[*] Planificando ruta de evacuación hacia la base {BASE} con A*...")
        camino_retorno = planificar_retorno_a_estrella(self.cuadricula, self.posicion, BASE)
        print(f"    Ruta encontrada ({len(camino_retorno)} pasos): {camino_retorno}")

        for paso in camino_retorno[1:]:
            self.posicion = paso
            self.pasos_totales += 1
            self.bateria -= 0.5 # Consumo eficiente en modo retorno

        print(f"[+] Robot seguro en Base {BASE}. Batería restante al llegar: {self.bateria:.1f}%")
        print("[*] Recargando baterías en la estación al 100%...")
        self.bateria = 100.0
        self.ciclos_recarga += 1
        print("[+] Recarga completada. Reanudando cobertura del mapa.\n")

    def renderizar_mapa(self):
        print("\n--- Visualización de la Cuadrícula ---")
        simbolos = {CELDA_LIMPIA: ".", CELDA_SUCIA: "S", CELDA_OBSTACULO: "#"}
        for r in range(self.filas):
            fila_str = []
            for c in range(self.columnas):
                if (r, c) == BASE:
                    fila_str.append("B")
                elif (r, c) == self.posicion:
                    fila_str.append("R")
                else:
                    fila_str.append(simbolos[self.cuadricula[r][c]])
            print("  " + " ".join(fila_str))
        print("  Leyenda: B=Base, R=Robot, .=Limpia, S=Sucia, #=Obstáculo\n")


def main():
    print("=" * 75)
    print("  TECNM / ITSU - ROBOT LIMPIADOR AUTÓNOMO (BOUSTROPHEDON + A*)")
    print("=" * 75)

    robot = RobotLimpiador(filas=7, columnas=7, bateria_inicial=65.0)
    # Colocar obstáculos interiores (muebles, paredes)
    obstaculos = [(1, 2), (2, 2), (3, 2), (5, 4), (5, 5)]
    robot.sembrar_obstaculos(obstaculos)

    print("Estado inicial del entorno:")
    robot.renderizar_mapa()

    robot.ejecutar_ciclo_limpieza()

    print("\n" + "=" * 75)
    print("  CONSIDERACIONES ÉTICAS EN ROBÓTICA AUTÓNOMA Y DE SERVICIO")
    print("=" * 75)
    print("""
    1. Seguridad Humana e Integridad Física (Leyes de Asimov / ISO 13482):
       El robot debe detenerse o ralentizarse ante la detección de mascotas o personas
       en su camino, priorizando la evasión pasiva sobre la cobertura de tareas.
    2. Privacidad y Mapeo del Hogar: Las aspiradoras y robots autónomos generan planos
       espaciales íntimos de los hogares. Estos mapas no deben ser monetizados ni enviados
       a servidores externos sin cifrado y consentimiento expreso.
    3. Eficiencia y Sostenibilidad Energética: El algoritmo de retorno A* optimiza
       la vida útil de las baterías de litio y evita el desgaste prematuro de componentes.
    """)


if __name__ == "__main__":
    main()
