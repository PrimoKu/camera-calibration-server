import os
import cv2
import numpy as np
import socket
import time

from SingleCalibration import camera_calibration

def find_image_files(base_path, prefix, count):
    """
    Find and return a list of image file paths with a given prefix and count.
    
    :param base_path: The directory containing the image files.
    :param prefix: The prefix for the image files (typically 'LEFT' or 'RIGHT').
    :param count: The number of image files to find.
    :return: A list of file paths.
    """
    image_files = []
    for i in range(1, count + 1):
        filename = os.path.join(base_path, f"{prefix}_{i}.png")
        if os.path.exists(filename):
            image_files.append(filename)
        else:
            print(f"Missing image file: {filename}")
            break
    return image_files

def stereo_calibration(left_images, right_images, square_size, pattern_size):
    """
    Perform stereo camera calibration given the image sets from both cameras.
    
    :param left_images: Image paths for the left camera.
    :param right_images: Image paths for the right camera.
    :param square_size: Size of the chessboard square.
    :param pattern_size: Chessboard pattern (width, height).
    :return: None
    """

    # Calibrate the left camera
    print("Calibrating left camera...")
    _, mtx_left, dist_left = camera_calibration(left_images, square_size, pattern_size, "LEFT")

    # Calibrate the right camera
    print("Calibrating right camera...")
    _, mtx_right, dist_right = camera_calibration(right_images, square_size, pattern_size, "RIGHT")

    # Prepare object points similar to the single camera calibration
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2) * square_size

    # Arrays to store object points and image points from both cameras
    objpoints = []
    imgpoints_left = []
    imgpoints_right = []

    # Iterate through pairs of images
    for img_left_path, img_right_path in zip(left_images, right_images):
        img_left = cv2.imread(img_left_path)
        img_right = cv2.imread(img_right_path)

        # Convert to grayscale
        gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners for both images
        ret_left, corners_left = cv2.findChessboardCorners(gray_left, pattern_size, None)
        ret_right, corners_right = cv2.findChessboardCorners(gray_right, pattern_size, None)

        # If corners are found in both images, refine and store them
        if ret_left and ret_right:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
            corners2_left = cv2.cornerSubPix(gray_left, corners_left, (11, 11), (-1, -1), criteria)
            corners2_right = cv2.cornerSubPix(gray_right, corners_right, (11, 11), (-1, -1), criteria)
            objpoints.append(objp)
            imgpoints_left.append(corners2_left)
            imgpoints_right.append(corners2_right)

    # Perform stereo calibration
    ret, mtx_left, dist_left, mtx_right, dist_right, R, T, E, F = cv2.stereoCalibrate(
        objpoints, imgpoints_left, imgpoints_right, mtx_left, dist_left, mtx_right, dist_right,
        gray_left.shape[::-1], criteria=criteria, flags=cv2.CALIB_FIX_INTRINSIC)

    np.savez('stereo_calibration_data.npz',
        rms_error=ret,                              # The root mean square (RMS) re-projection error.
        left_camera_matrix=mtx_left,                # The camera matrix for the left camera.
        left_distortion_coefficients=dist_left,     # The distortion coefficients for the left camera.
        right_camera_matrix=mtx_right,              # The camera matrix for the right camera.
        right_distortion_coefficients=dist_right,   # The distortion coefficients for the right camera.
        rotation_matrix=R,                          # The rotation matrix between the two camera coordinate systems.
        translation_vector=T,                       # The translation vector between the camera coordinate systems.
        essential_matrix=E,                         # The essential matrix.
        fundamental_matrix=F)                       # The fundamental matrix.
    
    print("Stereo calibration complete.")


def send_calibration_complete_signal():
    """
    Send a signal indicating the calibration process is complete.
    """
    attempts = 3
    for _ in range(attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', 12346))
                s.sendall(b'Calibration Complete')
                break
        except ConnectionRefusedError:
            time.sleep(1)

def main():
    """
    Main function to execute the calibration steps.
    """
    # Define the number of images, chessboard square size, and pattern
    image_num = 20
    square_size = 0.035
    pattern_size = (7, 10)

    # Find the image paths for left and right cameras
    left_images = find_image_files("LEFT", "LEFT", image_num)
    right_images = find_image_files("RIGHT", "RIGHT", image_num)

    # Calibrate each camera and then perform stereo calibration
    if len(left_images) == image_num and len(right_images) == image_num:

        print("Performing stereo calibration...")
        stereo_calibration(left_images, right_images, square_size, pattern_size)

        send_calibration_complete_signal()
    else:
        print("Not enough images for calibration. Found left: {}, right: {}.".format(len(left_images), len(right_images)))

if __name__ == "__main__":
    main()