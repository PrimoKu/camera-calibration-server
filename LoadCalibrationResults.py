import numpy as np

def load_camera_calibration_results(filename):
    # Load the NPZ file
    data = np.load(filename)

    # Extract calibration parameters
    camera_matrix = data['camera_matrix']
    distortion_coefficients = data['distortion_coefficients']
    rotation_vectors = data['rotation_vectors']
    translation_vectors = data['translation_vectors']

    # Print out the results and return them
    print("Camera Matrix:\n", camera_matrix)
    print("Distortion Coefficients:\n", distortion_coefficients)
    print("Rotation Vectors:\n", rotation_vectors)
    print("Translation Vectors:\n", translation_vectors)

def load_stereo_calibration_results(filename):
    # Load the NPZ file
    data = np.load(filename)

    # Extract calibration parameters
    rms_error = data['rms_error']
    left_camera_matrix = data['left_camera_matrix']
    # Reshape the left distortion coefficients to a 1D array
    left_distortion_coefficients = data['left_distortion_coefficients'].reshape(-1)
    right_camera_matrix = data['right_camera_matrix']
    # Reshape the right distortion coefficients to a 1D array
    right_distortion_coefficients = data['right_distortion_coefficients'].reshape(-1)
    rotation_matrix = data['rotation_matrix']
    # Reshape the translation vector to a 1D array
    translation_vector = data['translation_vector'].reshape(-1)
    essential_matrix = data['essential_matrix']
    fundamental_matrix = data['fundamental_matrix']

    # Print out the results
    print("RMS Error:", rms_error)
    print("Left Camera Matrix:\n", left_camera_matrix)
    print("Left Distortion Coefficients (1D):", left_distortion_coefficients)
    print("Right Camera Matrix:\n", right_camera_matrix)
    print("Right Distortion Coefficients (1D):", right_distortion_coefficients)
    print("Rotation Matrix:\n", rotation_matrix)
    print("Translation Vector (1D):", translation_vector)
    print("Essential Matrix:\n", essential_matrix)
    print("Fundamental Matrix:\n", fundamental_matrix)

    # Organize data into a dictionary for potential JSON serialization or other uses
    calibration_data = {
        'rms_error': rms_error.item(),  # Convert numpy type to Python scalar
        'left_camera_matrix': left_camera_matrix.tolist(),  # Convert numpy array to list
        'left_distortion_coefficients': left_distortion_coefficients.tolist(),  # Now 1D
        'right_camera_matrix': right_camera_matrix.tolist(),
        'right_distortion_coefficients': right_distortion_coefficients.tolist(),  # Now 1D
        'rotation_matrix': rotation_matrix.tolist(),
        'translation_vector': translation_vector.tolist(),  # Now 1D
        'essential_matrix': essential_matrix.tolist(),
        'fundamental_matrix': fundamental_matrix.tolist()
    }

    return calibration_data


# Replace 'stereo_calibration_data.npz' with the path to your .npz file
# load_stereo_calibration_results('stereo_calibration_data.npz')
# load_camera_calibration_results('left_calibration_data.npz')