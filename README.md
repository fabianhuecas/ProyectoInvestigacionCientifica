# 🔬 Proyecto: Investigación Científica (Quantum State Dynamics)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Simulación numérica de sistemas de espín cuántico (número de spines $N=8$), cálculo de gaps de energía estáticos y evolución temporal de estados bajo protocolos dinámicos y adiabáticos adaptados.

---

## 📌 Descripción General

En el archivo `ProyectoInvestigacion.py` se encuentra el programa desarrollado en Python que lleva a cabo todos los resultados.

La matriz de enlaces $J$ se genera en la función `generar_matriz_J` de forma aleatoria, pero la semilla es siempre la misma, con lo que los resultados son siempre los mismos a menos que se cambie la semilla en la línea:
```python
rng = np.random.default_rng(20)
```

---

## 🚀 Requisitos e Instalación

### Requisitos previos
Instala las librerías necesarias ejecutando:
```bash
pip install numpy scipy matplotlib
```

### Ejecución
Se puede ejecutar el código directamente y estas tres funciones actuarán directamente ofreciendo los resultados mencionados a continuación:
```bash
python ProyectoInvestigacion.py
```

---

## 🛠️ Estructura del Código y Módulos

### 1. Análisis Estático (`salida_datos_estatico()`)

Todo el proceso de análisis estático se lleva a cabo en la función `salida_datos_estatico()`. Dentro de esta función se tienen seleccionados los valores del número de spines $N=8$ y el número de puntos de lambda $M=200$, aunque se podrían modificar.

#### Resultados en pantalla:
- **Valor mínimo del gap**
- **Valor de lambda crítico**
- **Valor máximo de** $\left\langle \psi_{\text{exct}} \left\vert{} \frac{dH}{d\lambda} \right\vert{} \psi_0 \right\rangle$

#### Archivos generados:
Además, genera una serie de archivos que ayuda a entender mejor el sistema:

| Archivo | Contenido |
| :--- | :--- |
| `autoH0.txt` | Contiene el estado fundamental de $H_0$ |
| `auto1H1.txt` | Contiene el primer autoestado de mínima energía de $H_1$ |
| `auto2H1.txt` | Contiene el segundo autoestado de mínima energía de $H_1$ |
| `E0.txt`, `E1.txt`, `E2.txt`, `E3.txt` | Contienen el valor de los cuatro primeros niveles de energía respectivamente para todos los valores de $\lambda$ |
| `gap.txt` | Contiene el gap de energía entre nivel fundamental y primer nivel excitado accesible para cada valor de $\lambda$ |
| `dHdl.txt` | Contiene los valores de $\left\langle \psi_{\text{exct}} \left\vert{} \frac{dH}{d\lambda} \right\vert{} \psi_0 \right\rangle$ para cada $\lambda$ |

> ⏱️ **Tiempo de ejecución:** Todo este proceso no debería tardar más de 10 segundos.

---

### 2. Análisis Dinámico (`salida_datos_dinamica()`)

Todo el proceso de análisis dinámico se lleva a cabo en la función `salida_datos_dinamica()`. En este caso debe introducir por pantalla:
- **T:** Tiempo de cómputo (en el trabajo asociado: `90`).
- **M:** Número de puntos temporales (en el trabajo asociado: `20000`).

#### Resultados en pantalla:
Finalizado el proceso, por pantalla se ofrece:
- El intervalo temporal $dt$
- La fidelidad en el último paso temporal

#### Archivos generados:
Además, ofrece los resultados de fidelidad respecto del estado inicial y final en los archivos:
- `p0.txt`
- `p1.txt`

> ⏱️ **Rendimiento y tiempo de ejecución:** Con unos 20 000 puntos el proceso puede tardar más de 30 segundos. Esto es debido a que se escogen muchos términos en el desarrollo del estado según el operador de evolución temporal y se examina la norma para cada uno; con una restricción menos fuerte se podría acelerar por mucho el proceso.

---

### 3. Protocolo Adaptado (`salida_datos_dinamica_avanzado()`)

Todo el proceso asociado al protocolo avanzado se lleva a cabo en la función `salida_datos_dinamica_avanzado()`. Se pide por pantalla:
- **T:** Tiempo de cómputo.
- **M:** Número de puntos temporales.

#### Resultados en pantalla:
Finalizado el proceso, por pantalla se ofrece:
- El intervalo temporal $dt$
- La fidelidad en el último paso temporal
- El parámetro adiabático

#### Archivos generados:
Además, ofrece los resultados de fidelidad respecto del estado inicial y final en los archivos:
- `p0.txt`
- `p1.txt`

> ⏱️ **Tiempo de ejecución:** Los tiempos de ejecución son muy parecidos a los que se tienen en el Análisis Dinámico.

