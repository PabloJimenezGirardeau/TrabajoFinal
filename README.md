# Resolución y Generación Avanzada de Sudoku

Este proyecto es una herramienta interactiva para resolver y generar sudokus. Proporciona una interfaz gráfica para interactuar con los tableros, personalizar configuraciones, y visualizar el proceso de resolución en tiempo real.

## Características Principales

- **Resolución de Sudoku**: Resuelve tableros de Sudoku utilizando algoritmos avanzados de backtracking optimizado.
- **Generación de Sudoku**: Genera tableros con dificultades ajustables y asegura la unicidad de la solución.
- **Interfaz Gráfica (GUI)**: Basada en Tkinter, permite a los usuarios interactuar con el programa de manera intuitiva.
- **Visualización en Tiempo Real**: Muestra el progreso del algoritmo de resolución.

---

## Requisitos Previos

Antes de ejecutar el programa, asegúrate de tener instalados los siguientes requisitos:

- **Python 3.7 o superior**
- Bibliotecas necesarias:
  - `numpy`
  - `tkinter` (incluido en la mayoría de las distribuciones de Python)

Puedes instalar `numpy` ejecutando:

```bash
pip install numpy
```

---

## Cómo Usar el Programa

### 1. Ejecutar la Aplicación

El punto de entrada principal es el archivo `main.py`. Para iniciar la aplicación, ejecuta:

```bash
python main.py
```

### 2. Interfaz de Usuario

#### **Tablero de Sudoku**
- El tablero de 9x9 celdas permite ingresar valores manualmente o cargar un tablero generado aleatoriamente.
- Cada celda acepta únicamente valores entre 1 y 9.

#### **Controles Principales**

1. **Generar Tablero**:
   - Haz clic en el botón `Generate`.
   - Selecciona la dificultad en el menú desplegable (opciones: `easy`, `medium`, `hard`, `expert`).

2. **Resolver Tablero**:
   - Ingresa un tablero manualmente o usa uno generado.
   - Haz clic en el botón `Solve` para iniciar la resolución.
   - La solución se mostrará en tiempo real con visualizaciones de progreso.

3. **Borrar Tablero**:
   - Haz clic en el botón `Clear` para reiniciar el tablero a su estado inicial.

#### **Opciones de Configuración**

- **Velocidad de Resolución**:
  - Ajusta el control deslizante para cambiar la velocidad de visualización del algoritmo de resolución (más lento o más rápido).

---

## Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación.
- `sudoku_solver.py`: Contiene la lógica para resolver sudokus utilizando algoritmos avanzados.
- `sudoku_generator.py`: Implementa la generación de tableros con validación de unicidad.
- `sudoku_gui.py`: Define la interfaz gráfica y las interacciones del usuario.

---

## Notas

- Asegúrate de no cerrar la aplicación mientras el algoritmo está resolviendo un tablero para evitar bloqueos.
- Si un tablero no tiene solución, el programa mostrará un mensaje de error.

---

## Ejemplo de Uso

1. **Generar y Resolver un Tablero**:
   - Abre la aplicación.
   - Selecciona una dificultad (`medium` por defecto).
   - Haz clic en `Generate` para obtener un tablero.
   - Haz clic en `Solve` para ver cómo se resuelve.

2. **Resolver un Tablero Personalizado**:
   - Ingresa manualmente valores en las celdas.
   - Haz clic en `Solve` para resolverlo.

---






