# Stereo Camera Calibration Server

This repository provides a Python-based server for performing stereo camera calibration using images sent over TCP. It's designed to be camera-agnostic, allowing users to calibrate any stereo camera setup by sending pairs of images to the dedicated server.

## Prerequisites

Before running the server, ensure you have the following installed:
- Python 3.x
- OpenCV library (cv2)
- NumPy
- Socket and threading libraries (should be included with Python)

## Installation

Clone this repository to your local machine using:

```bash
git clone https://github.com/PrimoKu/stereo-camera-calibration-server.git
```

Navigate to the cloned directory:

```bash
cd stereo-camera-calibration-server
```

No additional installation is needed as the scripts use standard Python libraries and OpenCV.

## Usage

To start the stereo camera calibration process, follow these steps:

1. **Start the Server**: Run the `TcpServer.py` script to start the server.

   ```bash
   python TcpServer.py
   ```

   The server will start listening for image data on the specified port.

2. **Send Image Data**: From your stereo camera setup, send pairs of images to the server using TCP. Each image should be sent with a header indicating its sequence and side (left or right).

3. **Calibration Process**: Once the required number of image pairs is received, the server automatically triggers the `StereoCalibration.py` script to perform stereo calibration. The calibration results will be saved and a signal indicating completion will be sent back.

## Scripts

- **TcpServer.py**: Sets up a TCP server to receive images, saves them, and triggers the calibration process once enough data is collected.

- **StereoCalibration.py**: Performs individual camera calibrations followed by stereo calibration, saving the calibration parameters upon completion. This script can also be run independently using example images in the `LEFT` and `RIGHT` folders for testing purposes. Note that the quality of these example images is not ideal for a real calibration but serves for demonstration and testing.

- **LoadCalibrationResults.py**: This script is used to load and display the calibration results stored in an `.npz` file. It outputs the RMS error, camera matrices, distortion coefficients, rotation and translation matrices, and the essential and fundamental matrices.

## Test Calibration with Example Images

The repository includes two folders, `LEFT` and `RIGHT`, containing example stereo images. These images are for testing purposes and are not of high quality for actual calibration. To test the calibration script with these images, simply run:

```bash
python StereoCalibration.py
```

The script will process the example images and output the calibration results, which can then be viewed using the `LoadCalibrationResults.py` script.

## Configuration

- The number of image pairs required for calibration can be adjusted in `TcpServer.py` by modifying `required_image_count`.
- Calibration square size and pattern can be adjusted in `StereoCalibration.py`.

## Outputs

- The calibration parameters are saved in `stereo_calibration_parameters.npz` after the successful completion of the calibration process.
- The server and calibration scripts provide console output to indicate their status and results.

## Viewing Calibration Results

To view the calibration results, run the `LoadCalibrationResults.py` script:

```bash
python LoadCalibrationResults.py
```

Ensure that you update the script to point to the correct `.npz` file if it's not in the same directory or if it's named differently.

## Troubleshooting

- Ensure that the server and client are on the same network and the correct IP address and port are used.
- Verify that the images are sent in the correct format and order.
- Check console outputs for error messages and ensure all prerequisites are installed.