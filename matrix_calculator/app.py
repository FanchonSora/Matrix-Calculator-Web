from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def matrix_operations():
    result = None
    if request.method == 'POST':
        matrix_input = request.form['matrix']
        try:
            # Parse the input matrix
            matrix = []
            rows = matrix_input.strip().split('\n')
            for row in rows:
                matrix.append([float(num) for num in row.strip().split()])
            np_matrix = np.array(matrix)

            # Calculate determinant
            determinant = None
            if np_matrix.shape[0] == np_matrix.shape[1]:
                determinant = np.linalg.det(np_matrix)
            else:
                determinant = 'Not a square matrix'

            # Calculate inverse
            inverse = None
            if np_matrix.shape[0] == np_matrix.shape[1]:
                try:
                    inverse = np.linalg.inv(np_matrix)
                except np.linalg.LinAlgError:
                    inverse = 'Matrix is singular and cannot be inverted'
            else:
                inverse = 'Not a square matrix'

            # Calculate transpose
            transpose = np_matrix.T

            # Calculate rank
            rank = np.linalg.matrix_rank(np_matrix)

            result = {
                'determinant': determinant,
                'inverse': inverse if isinstance(inverse, str) else inverse.tolist(),
                'transpose': transpose.tolist(),
                'rank': rank
            }
        except Exception as e:
            result = {'error': str(e)}
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
