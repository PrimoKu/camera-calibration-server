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
    left_distortion_coefficients = data['left_distortion_coefficients']
    right_camera_matrix = data['right_camera_matrix']
    right_distortion_coefficients = data['right_distortion_coefficients']
    rotation_matrix = data['rotation_matrix']
    translation_vector = data['translation_vector']
    essential_matrix = data['essential_matrix']
    fundamental_matrix = data['fundamental_matrix']

    # Print out the results
    print("RMS Error:", rms_error)
    print("Left Camera Matrix:\n", left_camera_matrix)
    print("Left Distortion Coefficients:", left_distortion_coefficients)
    print("Right Camera Matrix:\n", right_camera_matrix)
    print("Right Distortion Coefficients:", right_distortion_coefficients)
    print("Rotation Matrix:\n", rotation_matrix)
    print("Translation Vector:", translation_vector)
    print("Essential Matrix:\n", essential_matrix)
    print("Fundamental Matrix:\n", fundamental_matrix)

# Replace 'stereo_calibration_data.npz' with the path to your .npz file
load_stereo_calibration_results('stereo_calibration_data.npz')

# load_camera_calibration_results('left_calibration_data.npz')