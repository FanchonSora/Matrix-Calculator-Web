from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

def parse_matrix(matrix_list):
    """Parse the matrix from a list of lists."""
    try:
        return np.array(matrix_list, dtype=float)
    except ValueError:
        raise ValueError("Invalid matrix format. Ensure all elements are numbers.")

def row_echelon(matrix):
    """Compute the row echelon form of a matrix."""
    mat = matrix.copy()
    rows, cols = mat.shape
    for i in range(min(rows, cols)):
        max_row = i + np.argmax(np.abs(mat[i:, i]))
        if mat[max_row, i] == 0:
            continue
        mat[[i, max_row]] = mat[[max_row, i]]  # Swap rows
        mat[i] = mat[i] / mat[i, i]  # Scale to make pivot = 1
        for j in range(i + 1, rows):
            mat[j] -= mat[i] * mat[j, i]
    return mat

@app.route('/', methods=['GET'])
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/', methods=['POST'])
def matrix_operations():
    """Handle matrix operations."""
    data = request.get_json()
    matrixA = data.get('matrixA')
    matrixB = data.get('matrixB')
    operation = data.get('operation')
    scalar = data.get('scalar', None)  
    power = data.get('power', None)   

    try:
        result = {}

        if matrixA:
            matrixA = parse_matrix(matrixA)
        else:
            raise ValueError("Matrix A is required.")

        if matrixB:
            matrixB = parse_matrix(matrixB)

        # Perform the requested operation
        if operation == 'multiply_scalar':
            if scalar is None:
                raise ValueError("Scalar value is required for scalar multiplication.")
            result['Matrix A * scalar'] = (matrixA * scalar).tolist()

        elif operation == 'determinant':
            if matrixA.shape[0] == matrixA.shape[1]:
                result['determinant_A'] = np.linalg.det(matrixA)
            else:
                result['determinant_A'] = "Matrix A is not square."
            if matrixB is not None and matrixB.shape[0] == matrixB.shape[1]:
                result['determinant_B'] = np.linalg.det(matrixB)
            else:
                result['determinant_B'] = "Matrix B is not square."

        elif operation == 'transpose':
            result['transpose_A'] = matrixA.T.tolist()
            if matrixB is not None:
                result['transpose_B'] = matrixB.T.tolist()

        elif operation == 'rank':
            result['rank_A'] = np.linalg.matrix_rank(matrixA)
            if matrixB is not None:
                result['rank_B'] = np.linalg.matrix_rank(matrixB)

        elif operation == 'A * B':
            if matrixB is not None and matrixA.shape[1] == matrixB.shape[0]:
                result['A * B'] = (matrixA @ matrixB).tolist()
            else:
                result['A * B'] = "Matrix multiplication not possible. Columns of A must equal rows of B."

        elif operation == 'A + B':
            if matrixB is not None and matrixA.shape == matrixB.shape:
                result['A + B'] = (matrixA + matrixB).tolist()
            else:
                result['A + B'] = "Matrices A and B must have the same dimensions for addition."

        elif operation == 'inverse':
            try:
                if matrixA.shape[0] == matrixA.shape[1]:
                    result['inverse_A'] = np.linalg.inv(matrixA).tolist()
                else:
                    result['inverse_A'] = "Matrix A is not square."
                if matrixB is not None and matrixB.shape[0] == matrixB.shape[1]:
                    result['inverse_B'] = np.linalg.inv(matrixB).tolist()
                else:
                    result['inverse_B'] = "Matrix B is not square."
            except np.linalg.LinAlgError:
                result['inverse_A'] = "Matrix A is singular and cannot be inverted."
                result['inverse_B'] = "Matrix B is singular and cannot be inverted."

        elif operation == 'row_echelon':
            result['row_echelon_A'] = row_echelon(matrixA).tolist()
            if matrixB is not None:
                result['row_echelon_B'] = row_echelon(matrixB).tolist()

        else:
            raise ValueError("Unsupported operation or invalid input.")

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
