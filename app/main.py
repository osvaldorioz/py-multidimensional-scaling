from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import numpy as np
from typing import List
import matplotlib
import matplotlib.pyplot as plt
import mds_module 
import json

matplotlib.use('Agg')  # Usar backend no interactivo
app = FastAPI()

# Definir el modelo para el vector
class VectorF(BaseModel):
    vector: List[float]
    
@app.post("/multidimensional-scaling")
def calculo(num_points: int, num_components: int):
    output_file_1 = 'mds-dispersion.png'
    output_file_2 = 'mds-varianza.png'
    
    # 🔹 Generar una matriz de distancias simétrica aleatoria de 10x10
    np.random.seed(42)  # Fijar la semilla para reproducibilidad
    size = num_points  # Número de puntos

    # Matriz de distancias aleatoria (simétrica y con ceros en la diagonal)
    random_distances = np.random.rand(size, size) * 10
    np.fill_diagonal(random_distances, 0)  # Distancia de un punto consigo mismo es 0
    distances = (random_distances + random_distances.T) / 2  # Hacerla simétrica

    # 🔹 Aplicar MDS con el módulo en C++
    n_components = num_components
    reduced_data = mds_module.multidimensional_scaling(distances, n_components)

    # 🔹 Crear nombres aleatorios para los puntos
    point_labels = [f"P{i+1}" for i in range(size)]

    # 🔹 Gráfico de dispersión
    plt.figure(figsize=(8, 6))
    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c='blue', marker='o')
    for i, label in enumerate(point_labels):
        plt.annotate(label, (reduced_data[i, 0], reduced_data[i, 1]), fontsize=12, color='red')
    plt.title('MDS - Gráfico de Dispersión')
    plt.xlabel('Componente 1')
    plt.ylabel('Componente 2')
    plt.grid(True)
    #plt.show()
    plt.savefig(output_file_1)

    # 🔹 Gráfico de varianza explicada (suponiendo una distribución aleatoria)
    explained_variance = np.sort(np.random.rand(n_components))[::-1]  # Simulación de varianza explicada
    explained_variance /= explained_variance.sum()  # Normalizar para que sumen 1

    plt.figure(figsize=(8, 6))
    plt.bar(range(1, n_components + 1), explained_variance, color='green', alpha=0.7)
    plt.title('Varianza Explicada por Componente')
    plt.xlabel('Componentes')
    plt.ylabel('Proporción de Varianza Explicada')
    plt.xticks(range(1, n_components + 1))
    #plt.show()

    plt.savefig(output_file_2)
    plt.close()
    
    j1 = {
        "Grafica de dispersion": output_file_1,
        "Grafica de varianza": output_file_2
    }
    jj = json.dumps(str(j1))

    return jj

@app.get("/multidimensional-scaling-graph")
def getGraph(output_file: str):
    return FileResponse(output_file, media_type="image/png", filename=output_file)
