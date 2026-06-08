#!/usr/bin/env python
# coding: utf-8

# In[33]:


import numpy as np
#import time


# In[34]:


def Bits_entero(N): #verified

    #Funcion que devuelve la secuencia de bits asociada a un entero

    if(N==0):

        return '0'

    #Primer termino 
    secuencia_bit = ""
    sumando = 0
    
    n = np.log2(N)

    secuencia_bit += "1"
    n = int(np.log2(N))
    sumando += 2**n
    
    for k in range(n-1,-1,-1):

        if(sumando+(2**(k))>N):

            secuencia_bit += "0"

        else:

            sumando += (2**(k))
            secuencia_bit += "1"
        
    return secuencia_bit


# In[4]:


def preparacion_sistema(N):

    #Obtencion de todas las secuencias del sistema con N particulas y dos posibles estados
    #cada secuencia representa un elemento de base 
    #cada secuencia es "i1i2i3....iN" si i = 0, representa el estado spin +1/2 y si i=+1, representa el estado spin -1/2

    num_secuencias = 2**N

    secuencias = [Bits_entero(i_sec).zfill(N) for i_sec in range(num_secuencias)]

    return secuencias
    


# In[5]:


def num_spins_coincidentes(sec1,sec2):

    #numero de estados de spins coincidentes entre dos elementos de base sec1 y sec2
    #se comparan estados monoparticulares

    N1 = len(sec1)
    N2 = len(sec2)

    if(N1!=N2): return 
    else:
        n_coincidentes = 0
        for i_sec in range(N1):

            if(sec1[i_sec]==sec2[i_sec]):

                n_coincidentes += 1

    return n_coincidentes


# In[6]:


def matriz_H0(N, secuencias):

    #N numero de particulas
    #secuencias: elementos de base identificados en secuencias

    num_elem = 2**N #al haber dos estados monoparticulares (spin) la dimension del hamiltoniano 2**N x 2**N

    H0 = np.zeros((num_elem,num_elem))

    for i in range(num_elem):
        sec_i = secuencias[i]
        for j in range(num_elem):

            sec_j = secuencias[j]

            num_spins_coin = num_spins_coincidentes(sec_i,sec_j)

            if((N-num_spins_coin==1)): #si se diferencian en un spin los estados se acoplan

                H0[i][j] = +1.0  
    return H0


# In[19]:


def generar_matriz_J(N):

    #Genera una matriz J NxN siguiendo una distribucion gaussiana

    num_elem_indp = int((N*(N-1))/2) #numero de elementos independientes de una matriz simetrica sin considerar la diagonal

    J = np.zeros((N,N)) #matriz J NxN

    rng = np.random.default_rng(20) #generamos semilla

    elementos = rng.normal(0.0, 1.0, size=num_elem_indp) #se toman los elementos independientes de la matriz segun distribucion gaussiano (0,1)

    #se llena la matriz teniendo en cuenta que es simetrica
    n = 0

    for fil in range(N):
        J[fil][fil]=0
        for col in range(fil):

            J[fil][col] = elementos[n]
            J[col][fil] = elementos[n]
            n+=1

    return J


# In[8]:


def matriz_H1(N,secuencias):

    #N numero de particulas
    #secuencias: elementos de base identificados en secuencias

    num_elem = 2**N

    H1 = np.zeros((num_elem,num_elem))

    J = generar_matriz_J(N) #matriz de enlaces

    for fil in range(num_elem): #H1 solo acopla un estado consigo mismo, es diagonal en esta base
        sec = secuencias[fil]
        elemento = 0
        #ahora vamos sumando el termino kJ_{ij}
        for i in range(N):
            for j in range(N):
                if(sec[i]==sec[j]):
                    k = 1 #si tienen mismos spines
                else:
                    k = -1 #si tienen spines opuestos

                elemento += k*J[i][j]

        H1[fil][fil] = elemento/N

    return H1


# In[9]:


def matriz_H(N,secuencias,lamda):

    #hamiltoniano total como: H = (1-lambda)H_0 + lambda*H_1

    H0 = matriz_H0(N,secuencias)
    H1 = matriz_H1(N,secuencias)

    H = (1-lamda)*H0 + lamda*H1

    return H


# In[10]:


def ordenar_con_indices(v):
    # Creamos los pares (índice, valor)
    pares = list(enumerate(v))
    
    # Modificamos la 'key' para que use abs(x[1])
    # Y ordena de mayor a menor valor absoluto con reverse
    pares_ordenados = sorted(pares, key=lambda x: abs(x[1]), reverse=True)
    
    # Separar valores e índices
    indices = [i for i, _ in pares_ordenados]
    valores = [val for _, val in pares_ordenados]
    
    return valores, indices


# In[11]:


def analisis_autoestado2(auto_estado,secuencias):

    #muestra el estado por pantalla ordenado segun su peso

    coefs, elementos_base = ordenar_con_indices(auto_estado)

    for coef, elemento in zip(coefs,elementos_base):

        print("Elemento: ",elemento,"secuencia: ",secuencias[elemento]," coef: ",np.abs(coef)**2)

    return


# In[35]:


def analisis_autoestado(auto_estado,secuencias):

    #muestra el estado por pantalla ordenado segun el peso del coeficiente

    coefs, elementos_base = ordenar_con_indices(auto_estado)

    for coef, elemento in zip(coefs,elementos_base):

        print("Elemento: ",elemento,"secuencia: ",secuencias[elemento]," coef: ",coef)

    return


# ## GAP REAL

# In[14]:


def gap(N,dH_dl,autovalores,auto_estados):

    '''
    Funcion que halla la diferencia de energia minima entre el estado fundamental y cualquier estado excitado
    accesible para un determinado hamiltoniano.

    Argumento:

    -N: numero de spines
    -dH_dl: es el operador necesario a evaluar
    -H: hamiltoniano del que extraer los autovectores

    Salida:

    - gap_i: diferencia de energia minima
    - valor_dHdl: valor de la cantidad dH_dl sobre los estados fundamental y excitado para la que se da

    '''
    
    num_elem = 2**N #dimension del espacio de Hilbert
    
     #obtenemos los autovalores y autovectores del hamiltoniano
    
    a0 = auto_estados[:,0] # autovector del nivel fundamental
    e0 = autovalores[0] #nivel de energia estado fundamental
    min_gap = 500 #referencia del minimo del gap que debe ser mayor a la magnitud de los resultados
    tol = 1e-10 #tolerancia para decidir si un estado es accesible o no
    
    for i in range(1,2**N):
        
        aexc = auto_estados[:,i] # estado i- excitado
        ei = autovalores[i] # nivel de nergia i-excitado
        
        valor_matriz = np.abs(aexc.T @ dH_dl @ a0) #Esto es <aexct | dH/dl | a0> 

        if(valor_matriz>tol): #si es mayor que la tolerancia se propone como el gap

            gap = np.abs(ei-e0)
        
            if(gap < min_gap): #si es menor que el gap hasta el momento es el nuevo gap
                
                gap_i = gap
                min_gap = gap
                valor_dHdl = valor_matriz

    return gap_i, valor_dHdl


# In[15]:


def gap_values(N,M):

    '''
    Funcion que halla el gap en todo el dominio de lambda [0,1]

    Argumentos:

    N: numero de spines
    M: numero de valores para lambda (mallado)

    Salida:

    gap: lista con los valores del gap para cada lambda
    lambdas: lista con todos los valores de lambda
    dH_dl: lista con todos los valores <aexct | dH/dl | a0>
    
    '''
    secuencias = preparacion_sistema(8)

    H0 = matriz_H0(N,secuencias) #matriz de H0 en base Z
    H1 = matriz_H1(N,secuencias) #matriz de H1 en base Z

    # Pre-calculamos la matriz derivada 
    dH_dl = -H0 + H1 

    #Mallado lambda
    lambdas = np.linspace(0,1,M)

    gap_vals = []
    dH_dl_lista = []

    list_E0 = []
    list_E1 = []
    list_E2 = []
    list_E3 = []

    #Para cada lambda buscamos el gap minimo
    for lamda in lambdas:
        
        H = (1-lamda)*H0 + lamda*H1 #construyo el hamiltoniano
        autovalores, auto_estados = np.linalg.eigh(H) #obtenemos todos los autovalores y autovectores

        list_E0.append(autovalores[0]) #tomo el del estado fundamental 
        list_E1.append(autovalores[1]) #tomo el del primer estado excitado
        list_E2.append(autovalores[2]) #tomo el del segundo estado excitado
        list_E3.append(autovalores[3]) #tomo el del tercer estado excitado
        
        gap_i, valdHdl = gap(N,dH_dl,autovalores,auto_estados) #obtengo el gap minimo para este lambda

        gap_vals.append(gap_i)
        dH_dl_lista.append(valdHdl)

        if(lamda==0):
            
            auto_H0 = auto_estados[:,0]

        elif(lamda==1.0):
            
            auto_H1 = auto_estados[:,0]
            auto2_H1 = auto_estados[:,1]

    return gap_vals, lambdas, dH_dl_lista, list_E0, list_E1, list_E2, list_E3, auto_H0, auto_H1, auto2_H1


# In[21]:


def salida_datos_estatico():

    #Funcion de llamada a funciones y salida de datos
    #Autovector fundamental de H0 en autoH0.txt
    #Autovectores fundamentales de H1 en auto1H1.txt y auto2H1.txt
    #Gap de energia en gap.txt
    #<psi_exct | dH/dlambda | psi_0> en dHdl.txt

    N = 8

    M = 200

    gap_vals, lambdas, dH_dl_lista, list_E0, list_E1, list_E2, list_E3, auto_H0, auto_H1, auto2_H1 = gap_values(N,M)

    nombre_archivos = ['autoH0','auto1H1','auto2H1']
    lista_autoestados = [auto_H0, auto_H1, auto2_H1]

    nom_arch_energias = ['E0','E1','E2','E3']
    lista_energias = [list_E0,list_E1,list_E2,list_E3]

    auto_total_H1 = (1/np.sqrt(2))*(auto_H1+auto2_H1)

    secuencias = preparacion_sistema(N)
    
    for auto_estado, nombre in zip(lista_autoestados,nombre_archivos):

        coefs, elementos_base = ordenar_con_indices(auto_estado)

        with open(nombre+'.txt', "w") as archivo:

            for coef, elemento in zip(coefs,elementos_base):

                archivo.write("Indice: "+str(elemento)+"  Elemento base: |"+secuencias[elemento]+">  coef: "+str(coef))
                archivo.write("\n")

    for energia, nombre in zip(lista_energias,nom_arch_energias):

        with open(nombre+'.txt', "w") as archivo:

            archivo.write("Lambda    |      E\n")

            for lamda, e in zip(lambdas,energia):

                archivo.write(str(lamda)+'    '+str(e))
                archivo.write("\n")

    with open('gap.txt','w') as archivo:

        archivo.write("Lambda    |      Gap\n")

        for lamda, gap_i in zip(lambdas,gap_vals):

            archivo.write(str(lamda)+'    '+str(gap_i))
            archivo.write("\n")

    with open('dHdl.txt','w') as archivo:

        archivo.write("Lambda    |      dHdl\n")

        for lamda, dH_dl in zip(lambdas,dH_dl_lista):

            archivo.write(str(lamda)+'    '+str(dH_dl))
            archivo.write("\n")

    K_max = max(dH_dl_lista)
    AE_min = min(gap_vals)
    pos_critica = np.argmin(gap_vals)
    lambda_critico = lambdas[pos_critica]

    print("Valor minimo del gap: ",AE_min)
    print("Valor de lambda critico: ",lambda_critico)
    print("Valor maximo de <psi_exct | dH/dlambda | psi_0>: ",K_max)

    return auto_H0, auto_total_H1, list_E0, list_E1, list_E2, list_E3


# In[36]:

print('ANÁLISIS ESTÁTICO: ')
print('\n')
#t_0 = time.time()
auto_H0, auto_total_H1, list_E0, list_E1, list_E2, list_E3 = salida_datos_estatico()
#t = time.time()-t_0
#print(f"Tiempo de ejecucion analisis estatico: {t:.6f} s")
print('\n')


# ## DINAMICA

# In[37]:


def protocolo_lineal_lambda(t,T):

    #protocolo lineal

    return t/T


# In[38]:


def func_psi_i(H_i, dt, psi_0, N, secuencias):

    '''
    Funcion que halla el valor de la funcion de onda a partir del conocimiento de la misma en un nodo temporal anterior.

    Argumentos:

    lamda_i(real): valor de lambda para el tiempo t_i
    dt(real): intervalo temporal
    psi_0: valor de la funcion de onda en tiempo inicial, debe tener P coeficientes
    N: numero de spines
    secuencias: elementos de la base z
    max_term: maximo numero de terminos en la sumatoria
    tol: tolerancia

    Output:

    psi: funcion de onda actualizada
    norma: norma de la funcion de onda
    '''

    max_term = 50
    tol_sq = 1e-6

    j = 1j

    termino_k = np.copy(psi_0).astype(complex)
    psi = np.copy(psi_0).astype(complex)

    k=1
    
    while(k<max_term):

        termino_k = (-1j * dt / k) * (H_i @ termino_k)
        
        psi += termino_k

        norma_k_sq = np.vdot(termino_k, termino_k).real

        if(norma_k_sq<tol_sq):

            break
        
        k+=1

    norma = np.linalg.norm(psi)

    psi = psi/norma

    return psi

def evolucion_dinamica(N, M,T,psi_i,secuencias):

    '''
    Funcion que ofrece la funcion de onda para un mallado temporal a partir del conocimiento de esta en un tiempo inicial

    Argumentos:

    N: numero de spines
    M: numero de puntos para el mallado temporal
    T: tiempo de computo total
    secuencias: elementos de base en la base z

    Output:

    t: mallado temporal
    PSI_s: lista con las funciones de onda para cada nodo temporal
    NORMAS: norma de la funcion de onda en cada nodo temporal

    '''

    H0 = matriz_H0(N, secuencias)
    H1 = matriz_H1(N, secuencias)

    dt = T/(M-1)
    print(f"El intervalo temporal es: {dt:.6f}")   

    t = np.linspace(dt,T,M-1)

    PSIs = []
    PSIs.append(psi_i)
    #NORMAS = []

    for t_i in t:

        lambda_i = protocolo_lineal_lambda(t_i,T)

        H = (1-lambda_i)*H0 + lambda_i*H1

        #NORMAS.append(norma_i)

        psi_i = func_psi_i(H, dt, psi_i, N, secuencias)
        PSIs.append(psi_i)

    coefs, elementos_base = ordenar_con_indices(PSIs[-1])

    with open('EstadoFinalDinamica.txt', "w") as archivo:

        for coef, elemento in zip(coefs,elementos_base):

            archivo.write("Indice: "+str(elemento)+"  Elemento bas: |"+secuencias[elemento]+">  coef: "+str(coef))
            archivo.write("\n")

    return t, PSIs

def prob(psi_ref, conjunto_psis):

    '''
    Probabilidades asociada a psi_ref dado el conjunto de soluciones en el mallado temporal

    '''

    p = []

    for psi in conjunto_psis:

        solapamiento = np.vdot(psi_ref,psi)

        p.append((np.abs(solapamiento))**2)

    return p


def salida_datos_dinamica(psi_0,psi_1):

    N = 8

    T = float(input('Inserte valor del tiempo de computo T: '))

    M = int(input('Inserte el numero de puntos temporales: '))

    secuencias = preparacion_sistema(8)
    
    t,psi_s = evolucion_dinamica(N, M,T, auto_H0,secuencias)
    p_0 = prob(psi_0,psi_s)
    p_1 = prob(psi_1,psi_s)

    with open('p0.txt', 'w') as archivo:
        archivo.write("t            |      p0\n")
    
        for t_i, p_0_i in zip(t, p_0):
            # f"{t_i:.6f}" asegura los 6 decimales float
            archivo.write(f"{t_i:.6f}    {p_0_i}\n")

    with open('p1.txt', 'w') as archivo:
        archivo.write("t            |      p1\n")
    
        for t_i, p_1_i in zip(t, p_1):
            # f"{t_i:.6f}" asegura los 6 decimales float
            archivo.write(f"{t_i:.6f}    {p_1_i}\n")
            
    return p_0, p_1, t


# In[39]:

print('ANÁLISIS DINÁMICO: ')
print('\n')
#t_0 = time.time()
p_0, p_1, t = salida_datos_dinamica(auto_H0,auto_total_H1)
#t_eje = time.time() - t_0

print(f"La fidelidad en el ultimo paso temporal es: {p_1[-1]:.6f}")  
#print(f"Tiempo de ejecucion analisis dinamico: {t_eje:.6f}") 
print('\n') 


# # ANALISIS DINAMICO AVANZADO

# In[25]:


def C(coef):

    a_2 = coef[0]
    a_1 = coef[1]
    a_0 = coef[2]

    raiz = np.sqrt(4*a_0*a_2-a_1*a_1)

    return -1.0*(2/raiz)*np.atan(a_1/raiz)


# In[26]:


def epsilon(T,coef,C,K):

    a_2 = coef[0]
    a_1 = coef[1]
    a_0 = coef[2]

    raiz = np.sqrt(4*a_0*a_2-a_1*a_1)

    f = (2/raiz)*np.atan((2*a_2+a_1)/raiz)+C

    return (K/T)*f


# In[27]:


def t(lamda, epsilon,coef,C):

    a_2 = coef[0]
    a_1 = coef[1]
    a_0 = coef[2]

    raiz = np.sqrt(4*a_0*a_2-a_1*a_1)

    f = (2/raiz)*np.atan((2*a_2*lamda+a_1)/raiz)+C

    return (1/epsilon)*f


# In[28]:


def protocolo_avanzado_lambda(t,coef,C,epsilon,K):

    a_2 = coef[0]
    a_1 = coef[1]
    a_0 = coef[2]

    r = np.sqrt(4*a_0*a_2-a_1*a_1)

    lamda = (r*np.tan(r*((epsilon*t/K-C)/2))-a_1)/(2*a_2)

    return lamda
    
    


# In[29]:


def evolucion_dinamica_avanzada(N, M,T,psi_i, secuencias,coef,K):

    '''
    Funcion que ofrece la funcion de onda para un mallado temporal a partir del conocimiento de esta en un tiempo inicial

    Argumentos:

    N: numero de spines
    M: numero de puntos para el mallado temporal
    T: tiempo de computo total
    secuencias: elementos de base en la base z

    Output:

    t: mallado temporal
    PSI_s: lista con las funciones de onda para cada nodo temporal
    NORMAS: norma de la funcion de onda en cada nodo temporal

    '''

    H0 = matriz_H0(N, secuencias)
    H1 = matriz_H1(N, secuencias)

    dt = T/(M-1)
    print(f"El intervalo temporal es: {dt:.6f}")

    t = np.linspace(dt,T,M-1)

    PSIs = [psi_i]
    #NORMAS = []
    CC = C(coef)
    e = epsilon(T,coef,CC,K)

    print(f"El valor del parametro adiabatico epsilon es:  {e:.6f}")
    for t_i in t:

        lambda_i = protocolo_avanzado_lambda(t_i,coef,CC,e,K)

        H = (1-lambda_i)*H0 + lambda_i*H1

        psi_i = func_psi_i(H, dt, psi_i, N, secuencias)

        PSIs.append(psi_i)

    coefs, elementos_base = ordenar_con_indices(PSIs[-1])

    with open('EstadoFinalDinamicaAvanzado.txt', "w") as archivo:

        for coef, elemento in zip(coefs,elementos_base):

            archivo.write("Indice: "+str(elemento)+"  Elemento bas: |"+secuencias[elemento]+">  coef: "+str(coef))
            archivo.write("\n")

    return t, PSIs


# In[30]:


def salida_datos_dinamica_avanzado(psi_0,psi_1):

    coef = [19.13809917, -30.35512844,  12.16130874]

    N = 8

    T = float(input('Inserte valor del tiempo de computo T: '))

    M = int(input('Inserte el numero de puntos temporales: '))

    K = 1.75

    secuencias = preparacion_sistema(8)
    
    t, psi_s = evolucion_dinamica_avanzada(N, M, T,psi_0, secuencias,coef,K)
    p_0 = prob(psi_0,psi_s)
    p_1 = prob(psi_1,psi_s)

    with open('p0avanzado.txt', 'w') as archivo:
        archivo.write("t            |      p0\n")
    
        for t_i, p_0_i in zip(t, p_0):
            # f"{t_i:.6f}" asegura los 6 decimales float
            archivo.write(f"{t_i:.6f}    {p_0_i}\n")

    with open('p1avanzado.txt', 'w') as archivo:
        archivo.write("t            |      p1\n")
    
        for t_i, p_1_i in zip(t, p_1):
            # f"{t_i:.6f}" asegura los 6 decimales float
            archivo.write(f"{t_i:.6f}    {p_1_i}\n")
            
    return p_0, p_1, t


# In[31]:

print('PROTOCOLO ADPATADO: ')
print('\n')
#t_0 = time.time()
p0,p1,t = salida_datos_dinamica_avanzado(auto_H0,auto_total_H1)
#t_eje = time.time() - t_0

print(f"La fidelidad en el ultimo paso temporal es: {p1[-1]:.6f}")  
#print(f"Tiempo de ejecucion analisis dinamico avanzado: {t_eje:.6f}")  
print('\n')

