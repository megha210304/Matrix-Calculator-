import streamlit as st
import numpy as np

# Set page title
st.title('Matrix Operations Visualizer')

# Add description
st.write("""
This app allows you to perform various matrix operations using NumPy.
Select the operation you want to perform and input the matrices below.
""")

# Sidebar for operation selection
st.sidebar.header('Select Operation')
operation = st.sidebar.selectbox(
    'Choose a matrix operation',
    ['Addition', 'Subtraction', 'Multiplication', 'Transpose', 'Determinant', 'Inverse']
)

# Function to create matrix input
def create_matrix_input(label, key_prefix, default_rows=2, default_cols=2, max_dim=5):
    st.subheader(f'{label}')
    
    # Matrix dimensions
    col1, col2 = st.columns(2)
    rows = col1.number_input(f'Number of rows for {label}', min_value=1, max_value=max_dim, value=default_rows, key=f'{key_prefix}_rows')
    cols = col2.number_input(f'Number of columns for {label}', min_value=1, max_value=max_dim, value=default_cols, key=f'{key_prefix}_cols')
    
    # Create matrix input fields
    matrix = []
    for i in range(int(rows)):
        row = []
        cols_input = st.columns(int(cols))
        for j in range(int(cols)):
            row.append(cols_input[j].number_input(f'', value=0, key=f'{key_prefix}_{i}_{j}'))
        matrix.append(row)
    
    return np.array(matrix)

# Create input for Matrix A
matrix_a = create_matrix_input('Matrix A', 'a')

# For operations that require two matrices
if operation in ['Addition', 'Subtraction', 'Multiplication']:
    # For multiplication, set default columns of B to match rows of A
    default_cols_b = 2
    if operation == 'Multiplication':
        st.info('For matrix multiplication, the number of columns in Matrix A must equal the number of rows in Matrix B.')
        default_cols_b = matrix_a.shape[0]
    
    # Create input for Matrix B with appropriate dimensions
    matrix_b = create_matrix_input('Matrix B', 'b', default_rows=matrix_a.shape[1], default_cols=default_cols_b)

# Perform the selected operation when the button is clicked
if st.button('Perform Operation'):
    try:
        if operation == 'Addition':
            if matrix_a.shape != matrix_b.shape:
                st.error('Matrices must have the same dimensions for addition.')
            else:
                result = np.add(matrix_a, matrix_b)
                st.success('Matrix Addition Result:')
                st.dataframe(result)
        
        elif operation == 'Subtraction':
            if matrix_a.shape != matrix_b.shape:
                st.error('Matrices must have the same dimensions for subtraction.')
            else:
                result = np.subtract(matrix_a, matrix_b)
                st.success('Matrix Subtraction Result:')
                st.dataframe(result)
        
        elif operation == 'Multiplication':
            if matrix_a.shape[1] != matrix_b.shape[0]:
                st.error('Number of columns in Matrix A must equal number of rows in Matrix B for multiplication.')
            else:
                result = np.matmul(matrix_a, matrix_b)
                st.success('Matrix Multiplication Result:')
                st.dataframe(result)
        
        elif operation == 'Transpose':
            result = matrix_a.T
            st.success('Matrix Transpose Result:')
            st.dataframe(result)
        
        elif operation == 'Determinant':
            if matrix_a.shape[0] != matrix_a.shape[1]:
                st.error('Matrix must be square to calculate determinant.')
            else:
                result = np.linalg.det(matrix_a)
                st.success(f'Determinant Result: {result}')
        
        elif operation == 'Inverse':
            if matrix_a.shape[0] != matrix_a.shape[1]:
                st.error('Matrix must be square to calculate inverse.')
            else:
                try:
                    result = np.linalg.inv(matrix_a)
                    st.success('Matrix Inverse Result:')
                    st.dataframe(result)
                except np.linalg.LinAlgError:
                    st.error('This matrix is not invertible (singular matrix).')
    
    except Exception as e:
        st.error(f'An error occurred: {str(e)}')

# Add information about the app
st.sidebar.markdown('---')
st.sidebar.subheader('About')
st.sidebar.info("""
This app demonstrates various matrix operations using NumPy and Streamlit.

Operations supported:
- Addition
- Subtraction
- Multiplication
- Transpose
- Determinant
- Inverse
""")