import os
import cv2
import numpy as np
import socket
import time

def find_image_files(base_path, prefix, count):
    """
    Find and return a list of image file paths with a given prefix and count.
    
    :param base_path: The directory containing the image files.
    :param prefix: The prefix for the image files (typically 'CAMERA_SIDE').
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

def camera_calibration(images, square_size, pattern_size, prefix):
    """
    Perform calibration for a single camera using chessboard images.
    
    :param images: The list of image paths used for calibration.
    :param square_size: The size of one square on the chessboard.
    :param pattern_size: The number of squares on the chessboard (width, height).
    :return: The camera matrix and distortion coefficients.
    """
    # Prepare object points based on the chessboard pattern and size
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2) * square_size

    # Arrays to store object points and image points
    objpoints = []  # 3d points in real world space
    imgpoints = []  # 2d points in image plane

    # Iterate over the images and find chessboard corners
    for img_path in images:
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        # If found, refine the corner positions and store the points
        if ret:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            objpoints.append(objp)
            imgpoints.append(corners2)

    # Calibrate the camera and return the results
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    np.savez(f"{prefix.lower()}_calibration_data.npz",
             camera_matrix=mtx,
             distortion_coefficients=dist,
             rotation_vectors=rvecs,
             translation_vectors=tvecs)

    print(f"Single calibration complete.")
    return ret, mtx, dist

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
    Main function to execute the camera calibration steps.
    """
    image_num = 20
    square_size = 0.035
    pattern_size = (7, 10)

    image_files = find_image_files("LEFT", "LEFT", image_num)
    camera_calibration(image_files, square_size, pattern_size, "LEFT")

    send_calibration_complete_signal()

if __name__ == "__main__":
    main()