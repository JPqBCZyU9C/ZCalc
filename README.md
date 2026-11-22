# ZCalc

Calculadora de escritorio desarrollada con Python y GTK 4.

## Funciones

- Suma, resta, multiplicación y división, respetando la prioridad de operaciones.
- Números decimales, cambio de signo, porcentaje y borrado de dígitos.
- Uso mediante botones o teclado.
- Manejo de división entre cero.
- Interfaz oscura diseñada para escritorio.

## Requisitos

- Python 3 y GTK 4 con sus bindings de PyGObject.

```bash
sudo apt update
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-4.0
```

## Ejecutar

Desde la carpeta del proyecto:

```bash
python3 main.py
```

## Atajos de teclado

| Tecla | Acción |
|---|---|
| `0`–`9` | Introducir cifras |
| `+`, `-`, `*`, `/` | Operaciones |
| `.` o `,` | Separador decimal |
| `Enter` o `=` | Calcular |
| `Backspace` | Borrar último carácter |
| `Esc` o `Supr` | Limpiar |

## Pruebas

```bash
python3 -m unittest discover -s tests -v
