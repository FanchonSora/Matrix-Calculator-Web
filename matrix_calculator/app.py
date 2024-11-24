from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

def parse_matrix(matrix_str):
    rows = matrix_str.strip().split('\n')
    return np.array([[float(num) for num in row.split()] for row in rows])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def matrix_operations():
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

        if operation == 'determinant' and matrixA.shape[0] == matrixA.shape[1]:
            result['determinant_A'] = np.linalg.det(matrixA)
            if matrixB is not None and matrixB.shape[0] == matrixB.shape[1]:
                result['determinant_B'] = np.linalg.det(matrixB)

        elif operation == 'transpose':
            result['transpose_A'] = matrixA.T.tolist()
            if matrixB is not None:
                result['transpose_B'] = matrixB.T.tolist()

        elif operation == 'rank':
            result['rank_A'] = np.linalg.matrix_rank(matrixA)
            if matrixB is not None:
                result['rank_B'] = np.linalg.matrix_rank(matrixB)

        elif operation == 'inverse':
            try:
                result['inverse_A'] = np.linalg.inv(matrixA).tolist()
                result['inverse_B'] = np.linalg.inv(matrixB).tolist()
            except np.linalg.LinAlgError:
                result['inverse_A'] = "Matrix A is singular"
                result['inverse_B'] = "Matrix B is singular"

        else:
            result['error'] = "Unsupported operation or invalid matrix input."

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
