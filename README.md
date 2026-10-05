# Actividad 26: Diseña tu Primer Robot Virtual (Robot Limpiador Autónomo)

**Tecnológico Nacional de México**  
**Instituto Tecnológico Superior de Uruapan**  
**División de Estudios de Posgrado e Investigación**  
**Maestría en Inteligencia Artificial**  

* **Asignatura:** Inteligencia Artificial y su Ética  
* **Alumno:** Juan Pablo Figueroa Moran  
* **Matrícula:** M26040059  
* **Repositorio Oficial:** [IAE_U4_A26_Robotica_Limpiador_Autonomo](https://github.com/juanpablofm92/IAE_U4_A26_Robotica_Limpiador_Autonomo)

---

## 🏢 1. Contexto Profesional y Misión
Eres un ingeniero en un startup que desarrolla robots de servicio para hogares inteligentes.

### Tu Misión:
1. **Diseñar el comportamiento:** Programar un robot que pueda limpiar una habitación eficientemente con cobertura completa.
2. **Implementar navegación:** Desarrollar algoritmos para evitar obstáculos domésticos (muebles, paredes intermedias).
3. **Optimizar rutas:** Encontrar la ruta más eficiente para cubrir toda el área (barrido Boustrophedon y retorno energético con algoritmo A*).

---

## 🧩 2. Arquitectura del Código y Plantilla Base

El sistema implementa estrictamente la estructura y firma solicitada:

```python
def proyecto_robot_limpiador():
    """Plantilla para el proyecto del robot limpiador"""
    print(" Proyecto: Robot Limpiador Autónomo")

    class RobotLimpiador(RobotAutonomo):
        def __init__(self, nombre, ancho=7, alto=7):
            super().__init__(nombre)
            self.areas_limpias = set()
            self.bateria = 100
            self.capacidad_basura = 100
            ...
        def limpiar_area(self, x, y):
            ...
        def planificar_ruta_limpieza(self, ancho, alto):
            ...
    return RobotLimpiador

RobotLimpiador = proyecto_robot_limpiador()
```

### Componentes Clave:
* **`RobotAutonomo`:** Clase base con primitivas cinemáticas, sensor de proximidad y gestión del estado del agente.
* **Cobertura Boustrophedon (Patrón Serpiente):** Garantiza visita metódica celda a celda sin solapamientos ni celdas omitidas.
* **Retorno Informado A\* Heurístico:**
  $$f(n) = g(n) + h(n), \quad h(n) = |x_n - x_{base}| + |y_n - y_{base}|$$
  Se activa automáticamente cuando $\text{batería} \le 20\%$, evacuando el robot hacia la base `(0, 0)` esquivando obstáculos de forma óptima.

---

## 📊 3. Rúbrica de Evaluación Académica

| Categoría | Excelente (4.5 - 5.0) | Satisfactorio (4.0 - 4.4) | En Desarrollo (3.5 - 3.9) |
| :--- | :--- | :--- | :--- |
| **Preprocesamiento** | Entorno matricial parametrizado, validación de coordenadas y control de colisiones. | Preprocesamiento adecuado de celdas. | Técnicas básicas implementadas. |
| **Modelado** | Boustrophedon óptimo integrado con búsqueda heurística A* de retorno energético. | Modelo funcional y preciso. | Modelo básico implementado. |
| **Evaluación** | 100% de cobertura de celdas transitables, telemetría de pasos y consumo energético. | Evaluación adecuada. | Métricas básicas calculadas. |
| **Documentación** | Código modular, tipado estático, consideraciones éticas ISO 13482 y README exhaustivo. | Documentación clara. | Documentación mínima. |

---

## 🚀 4. Instalación y Ejecución

```bash
# Clonar repositorio
git clone https://github.com/juanpablofm92/IAE_U4_A26_Robotica_Limpiador_Autonomo.git
cd IAE_U4_A26_Robotica_Limpiador_Autonomo

# Ejecutar simulación
python cleaning_robot.py
```

---

## ⚖️ 5. Consideraciones Éticas en Robótica de Servicio (ISO 13482)
1. **Seguridad Física:** Mecanismos de parada inmediata ante presencia de personas vulnerables y mascotas.
2. **Privacidad de Mapas Topográficos:** Cifrado local de la cartografía doméstica; prohibición de telemetría a la nube no autorizada.
3. **Sostenibilidad Energética:** Mitigación del envejecimiento de baterías de iones de litio mediante perfiles de recarga inteligentes.
