# 🔬 Proyecto: Investigación Científica (Quantum State Dynamics)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/Docs-GitHub%20Pages-brightgreen)](https://your-username.github.io/your-repo-name)

Numerical simulation of quantum spin systems ($N=8$), static energy gaps, and time-dependent state evolution under dynamic and adaptive adiabatic protocols.

---

## 📌 Overview

This repository implements the static and dynamic analysis of quantum spin systems governed by Hamiltonians $H_0$ and $H_1$. The coupling matrix $J$ is generated randomly using a deterministic seed (`rng = np.random.default_rng(20)`) to ensure exact numerical reproducibility across runs.

Key theoretical metrics evaluated:
- Energy levels: $E_0(\lambda), E_1(\lambda), E_2(\lambda), E_3(\lambda)$
- Minimum energy gap ($E_{\text{gap}}$):
  $$E_{\text{gap}} = \min_\lambda \left( E_1(\lambda) - E_0(\lambda) \right)$$
- Matrix elements for state transitions:
  $$\left\langle \psi_{\text{exct}} \left\vert{} \frac{dH}{d\lambda} \right\vert{} \psi_0 \right\rangle$$

---



# Proyecto Investigacion Cientifica

En el archivo ProyectoInvestigacion.py se encuentra el programa desarrollado en Python que lleva a cabo todos los resultados.

La matriz de enlaces J se genera en la funcion generar_matriz_J de forma aleatoria pero la semilla es siempre la misma con lo que los resultados
son siempre los mismos a menos que se cambie la semilla en la linea rng = np.random.default_rng(20).

## Análisis estático

Todo el proceso de análisis estático se lleva a cabo en la función salida_datos_estatico(). Dentro de esta función se tienen seleccionados 
los valores del número de spines N=8 y el número de puntos de lambda M=200 aunque se podrían modificar. Los resultados que se muestran en pantalla son:

- Valor mínimo del gap
- Valor de lambda crítico
- Valor máximo de <psi_exct | dH/dlambda | psi_0>

Además genera una serie de archivos que ayuda a entender mejor el sistema:

- 'autoH0.txt' contiene el estado fundamental de H0
- 'auto1H1.txt' y 'auto2H1.txt' contienen los dos autoestados de minima energía de H1
- 'E0.txt', 'E1.txt', 'E2.txt', 'E3.txt' contienen el valor de los cuatro primeros niveles de energia respectivamente para todos los valores de lambda.
- 'gap.txt' contiene el gap de energia entre nivel fundamental y primer nivel excitado accesible para cada valor de lambda.
- 'dHdl.txt' contiene los valores de <psi_exct | dH/dlambda | psi_0> para cada lambda.

Todo este proceso no debería tardar más de 10 segundos.

## Análisis dinámico.

Todo el proceso de análisis dinámico se lleva a cabo en la función salida_datos_dinamica. En este caso debe introducir por pantalla:

- T: tiempo de computo. (En el trabajo asociado: 90).
- M: numero de puntos temporales. (En el trabajo asociado: 20000).

Finalizado el proceso, por pantalla se ofrece: el intervalo temporal dt y la fidelidad en el ultimo paso temporal. Además, ofrece los resultados
de fidelidad respecto del estado inicial y final en los archivos 'p0.txt' y 'p1.txt'. Con unos 20000 puntos el proceso puede tardar mas de 30 segundos. 
Esto es debido a que se escogen muchos términos en el desarrllo del estado segun el operador de evolucion temporal y se examina la norma para cada uno,
con una restriccion menos fuerte se podria acelerar por mucho el proceso.

## Protocolo adaptado. 

Todo el proceso asociado al protocolo avanzado se lleva a cabo en la función salida_datos_dinamica_avanzado. Se pide por pantalla:

- T: tiempo de computo. 
- M: numero de puntos temporales. 

Finalizado el proceso, por pantalla se ofrece: el intervalo temporal dt, la fidelidad en el ultimo paso temporal y el parametro adiabático.  Además, ofrece los resultados de fidelidad respecto del estado inicial y final en los archivos 'p0.txt' y 'p1.txt'. Los tiempos de ejecución son muy parecidos a los que se tienen
en el Análisis Dinámico.

### Ejecucción

Se puede ejecutar el código y estas tres funciones actuarán directamente ofreciendo los resultados mencionados.

