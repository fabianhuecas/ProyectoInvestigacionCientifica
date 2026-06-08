# ProyectoInvestigacionCientifica

En el archivo ProyectoInvestigacion.py se encuentra el programa desarrollado en Python que lleva a cabo todos los resultados.

La matriz de enlaces J se genera en la funcion generar_matriz_J de forma aleatoria pero la semilla es siempre la misma con los resultados
son siempre los mismos a menos que se cambia la linea rng = np.random.default_rng(20).

### Análisis estático

Todo el proceso de análisis estático se lleva a cabo en la función salida_datos_estatico(). Dentro de esta función se tienen seleccionados 
los valores del número de spines N=8 y el número de puntos de lambda M=200 aunque se podrían modificar. Los resultados que se muestran en pantalla son:

- Valor minimo del gap
- Valor de lambda critico
- Valor maximo de <psi_exct | dH/dlambda | psi_0>

Además genera una serie de archivos que ayuda a entender mejor el sistema:

- 'autoH0.txt' contiene el estado fundamental de H0
- 'auto1H1.txt' y 'auto2H1.txt' contienen los dos autoestados de minima energía de H1
- 'E0.txt', 'E1.txt', 'E2.txt', 'E3.txt' contienen el valor de los cuatro primeros niveles de energia respectivamente para todos los valores de lambda.
- 'gap.txt' contiene el gap de energia entre nivel fundamental y primer nivel excitado accesible para cada valor de lambda.
- 'dHdl.txt' contiene los valores de <psi_exct | dH/dlambda | psi_0> para cada lambda.

Todo este proceso no debería tardar más de 10 segundos.

### Análisis dinámico.

Todo el proceso de análisis dinámico se lleva a cabo en la función salida_datos_dinamica. En este caso debe introducir por pantalla:

- T: tiempo de computo. (En el trabajo asociado: 90).
- M: numero de puntos temporales. (En el trabajo asociado: 20000).

Finalizado el proceso, por pantalla se ofrece: el intervalo temporal dt y la fidelidad en el ultimo paso temporal. Además, ofrece los resultados
de fidelidad respecto del estado inicial y final en los archivos 'p0.txt' y 'p1.txt'. Con unos 20000 puntos el proceso puede tardar mas de 30 segundos. 
Esto es debido a que se escogen muchos términos en el desarrllo del estado segun el operador de evolucion temporal y se examina la norma para cada uno,
con una restriccion menos fuerte se podria acelerar por mucho el proceso.

### Protocolo adaptada. 

Todo el proceso asociado al protocolo avanzado se lleva a cabo en la función salida_datos_dinamica_avanzado. Se pide por pantalla:

- T: tiempo de computo. 
- M: numero de puntos temporales. 

Finalizado el proceso, por pantalla se ofrece: el intervalo temporal dt, la fidelidad en el ultimo paso temporal y el parametro adiabático.  Además, ofrece los resultados de fidelidad respecto del estado inicial y final en los archivos 'p0.txt' y 'p1.txt'. Los tiempos de ejecución son muy parecidos a los que se tienen
en el Análisis Dinámico.

### Ejecucción

Se puede ejecutar el código y estas tres funciones actuarán directamente ofreciendo los resultados mencionados.

