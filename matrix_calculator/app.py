from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

def parse_matrix(matrix_list):
    """Parse the matrix from a list of lists."""
    return np.array(matrix_list, dtype=float)

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

    try:
        result = {}
        if matrixA:
            matrixA = parse_matrix(matrixA)

        if matrixB:
            matrixB = parse_matrix(matrixB)

        if operation == 'determinant':
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
            except np.linalg.LinAlgError as e:
                result['inverse_A'] = "Matrix A is singular and cannot be inverted."
                result['inverse_B'] = "Matrix B is singular and cannot be inverted."

        else:
            result['error'] = "Unsupported operation or invalid matrix input."

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
