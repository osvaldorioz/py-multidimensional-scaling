El Multidimensional Scaling (MDS) es un método de reducción de dimensionalidad que transforma una matriz de distancias entre puntos en un espacio de menor dimensión, preservando lo mejor posible las relaciones entre los puntos. Se usa en visualización de datos y análisis exploratorio.
📌 Pasos del Algoritmo MDS

    Entrada: Matriz de distancias DD entre NN puntos.
    Centrado doble:
        Se crea la matriz de centrado https://github.com/user-attachments/assets/8cdb143b-b1ac-4e73-8afe-af9936158657

        Se obtiene la matriz ![imagen](https://github.com/user-attachments/assets/a99fced1-988e-434b-90ff-d992be866a60)

    Descomposición en valores propios:
        Se calculan los valores y vectores propios de BB.
    Reducción de dimensión:
        Se seleccionan los kk mayores valores propios y sus vectores asociados.
        Se calculan las coordenadas en el nuevo espacio:
        ![imagen](https://github.com/user-attachments/assets/caafe8c8-e4ae-4dfd-990f-5bfb2cffe817)

    Salida: Matriz con las coordenadas de los puntos en el espacio de menor dimensión.

🔷 Implementación en C++ con Pybind11

    El microservicio python recibe una matriz de distancias desde Python como numpy.array y la convierte a una Eigen::MatrixXd.
    Calcula el MDS en C++ usando álgebra lineal con Eigen.
    Devuelve los datos a Python como un array NumPy.
    Visualiza los resultados en Python con gráficos de dispersión y varianza explicada.
