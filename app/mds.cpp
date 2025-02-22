#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <Eigen/Dense>
#include <vector>
#include <cmath>

namespace py = pybind11;
using namespace Eigen;

// Función para calcular el MDS
py::array_t<double> multidimensional_scaling(const py::array_t<double>& input_array, int n_components) {
    // Convertir el array de entrada a una matriz de Eigen
    auto buf = input_array.request();
    int n = buf.shape[0];

    MatrixXd distances(n, n);
    memcpy(distances.data(), buf.ptr, sizeof(double) * n * n);

    // Matriz de centrado H = I - (1/n) * J
    MatrixXd I = MatrixXd::Identity(n, n);
    MatrixXd ones = MatrixXd::Ones(n, n) / n;
    MatrixXd H = I - ones;

    // Matriz B = -0.5 * H * D^2 * H
    MatrixXd D_squared = distances.array().square();
    MatrixXd B = -0.5 * H * D_squared * H;

    // Descomposición en valores propios
    SelfAdjointEigenSolver<MatrixXd> solver(B);
    VectorXd eigenvalues = solver.eigenvalues().reverse();
    MatrixXd eigenvectors = solver.eigenvectors().rowwise().reverse();

    // Seleccionar las primeras `n_components` dimensiones
    VectorXd sqrt_eigenvalues = eigenvalues.head(n_components).cwiseSqrt();
    MatrixXd reduced_data = eigenvectors.leftCols(n_components) * sqrt_eigenvalues.asDiagonal();

    // Convertir la matriz a un array numpy
    std::vector<double> result_data(reduced_data.size());
    memcpy(result_data.data(), reduced_data.data(), sizeof(double) * reduced_data.size());

    return py::array_t<double>({n, n_components}, result_data.data());
}

// Exportar la función a Python usando Pybind11
PYBIND11_MODULE(mds_module, m) {
    m.def("multidimensional_scaling", &multidimensional_scaling, "Multidimensional Scaling",
          py::arg("distances"), py::arg("n_components") = 2);
}
