# Actividad 26: Robot Limpiador Autónomo con Boustrophedon y Retorno Seguro A*

**Tecnológico Nacional de México**  
**Instituto Tecnológico Superior de Uruapan**  
**División de Estudios de Posgrado e Investigación**  
**Maestría en Inteligencia Artificial**  

* **Asignatura:** Inteligencia Artificial y su Ética  
* **Alumno:** Juan Pablo Figueroa Moran  
* **Matrícula:** M26040059  

---

## 📌 1. Descripción del Proyecto

Este proyecto modela un agente robótico autónomo para cobertura completa de superficies interiores sobre una cuadrícula bidimensional $N \times M$.

### Componentes de Control:
1. **Patrón de Cobertura Boustrophedon (Serpiente / Escorpión):** Barrido metódico celda por celda alternando dirección este-oeste para maximizar el área higienizada minimizando giros innecesarios.
2. **Evasión de Obstáculos:** Detección de colisiones contra muros y mobiliario con replanificación local.
3. **Monitoreo Crítico de Batería:** Supervisión continua del nivel de carga energética; si la batería cae por debajo del **20%**, el agente suspende la tarea e invoca el algoritmo de búsqueda informada **A\*** con heurística Manhattan:
$$f(n) = g(n) + h(n), \quad h(n) = |x_n - x_{base}| + |y_n - y_{base}|$$
Una vez alcanzada la base en $(0,0)$, efectúa la recarga completa y retoma la limpieza.

---

## 🚀 2. Instalación y Ejecución

```bash
pip install -r requirements.txt
python cleaning_robot.py
```

---

## ⚖️ 3. Consideraciones Éticas en Robótica de Servicio

1. **Privacidad en el Hogar:** Los mapas y trayectorias generados por robots aspiradores representan datos espaciales sensibles que no deben compartirse con terceros ni alimentar bases de datos de mercadotecnia.
2. **Seguridad Operacional:** Prioridad absoluta a la integridad física de mascotas, niños y personas adultas mayores ante cualquier fallo sensorial del robot.
3. **Obsolescencia Programada y Baterías:** Diseño de políticas energéticas que mitiguen la degradación química de las celdas de litio.
