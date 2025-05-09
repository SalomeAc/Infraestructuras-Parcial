import json
from time import sleep
import pandas as pd

def cargarConfig():
    with open("config.json", "r") as f:
        config = json.load(f)  
    return [list(obj.values()) for obj in config]  

def simSecuencial(m, duracionEtapas):
    tiempoTotal = 0
 
    for i in range(m):
        for etapa in duracionEtapas:
            sleep(etapa/1000) # pasar a milisegundos
            tiempoTotal += etapa
            
    return tiempoTotal

def simPipelined(m, duracionEtapas):
    tiempoEtapaMasLenta= max(duracionEtapas)
    k = len(duracionEtapas) # etapas
    tiempoTotal = 0
    
    pipelineArr = ["-" for _ in range(k)]

    print("  ", end="")
    for i in range(k):
        print(f"    e{i + 1}", end="")
    print()
    
    for ciclo in range(m + k - 1):

        for i in range(k - 1, 0, -1):
            pipelineArr[i] = pipelineArr[i - 1] # se reemplaza por la que estaba antes
        
        if ciclo < m:
            pipelineArr[0] = f"I{ciclo + 1}"
        else:
            pipelineArr[0] = "-"


        print(f"{ciclo + 1}    |{pipelineArr}|")
    

        # etapa más lenta
        sleep(tiempoEtapaMasLenta / 1000)
        tiempoTotal += tiempoEtapaMasLenta
        
    return tiempoTotal
        
def speedup(m, duracionEtapas):
    resultados=[]

    for m in m:
        print(f"Simulación de m = {m} instrucciones:\n")

        tiempoSecuencial = simSecuencial (m, duracionEtapas)
        print(f"Tiempo secuencial: {tiempoSecuencial} ms\n")

        tiempoPipeline = simPipelined(m, duracionEtapas)
        print(f"Tiempo en pipeline: {tiempoPipeline} ms\n")

        speedup= tiempoSecuencial/tiempoPipeline
        print(f"Speedup: {speedup:.2f} \n")

        resultados.append((m, len(duracionEtapas), tiempoSecuencial, tiempoPipeline, speedup))
    return resultados

#borrar función

def exportarResultados(resultados, nombre_archivo):
    df = pd.DataFrame(resultados, columns=["m", "k", "Tiempo Secuencial (ms)", "Tiempo Pipelined (ms)", "Speedup"])
    df.to_excel(nombre_archivo, index=False)
    print(f"Resultados exportados a {nombre_archivo}")
    
def variacionM():
    print("Variando los valores de M:\n")
    resultado = speedup([5,10,20,25], cargarConfig()[0]) # este es el que se da en el parcial
    print("----------------------------------------------------------------")

    print("m\tk\tTiempo Secuencial\tTiempo Pipeline\tSpeedup")
    print("----------------------------------------------------------------")

      
    for m, k, tsecuencial, tpipelined, s in resultado:
        print(f"{m}\t{k}\t{tsecuencial:.2f}\t\t{tpipelined:.2f}\t\t{s:.2f}")

    exportarResultados(resultado, "variacionM.xlsx") # borrar

def variacionK(m, arregloEtapas):
    resultados = []
    print("Variando los valores de k:\n")

    for etapas in arregloEtapas:
        resultado = speedup(m, etapas)
        resultados.extend(resultado) 
    print("----------------------------------------------------------------")

    print("m\tk\tTiempo Secuencial\tTiempo Pipeline\tSpeedup")
    print("----------------------------------------------------------------")
    
    for m, k, tsecuencial, tpipelined, s in resultados:
        print(f"{m}\t{k}\t{tsecuencial:.2f}\t\t{tpipelined:.2f}\t\t{s:.2f}")
    exportarResultados(resultados, "variacionK.xlsx") # borrar

variacionM()
variacionK([6], cargarConfig())

