# Camera Calibration Server

This repository provides a Python-based server for performing camera calibration, supporting both single and stereo camera setups. Users can calibrate their camera systems by sending images to the server over TCP, making it adaptable for various camera configurations.

## Prerequisites

Before running the server, ensure you have the following installed:
- Python 3.x
- OpenCV library (cv2)
- NumPy
- Socket and threading libraries (included with Python)

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/PrimoKu/camera-calibration-server.git
```

Navigate to the cloned directory:

```bash
cd camera-calibration-server
```

No additional installation is needed as the scripts use standard Python libraries and OpenCV.

## Server Configuration Parameters

Before you start the server, you can configure the following parameters in `TcpServer.py` according to your setup:

- `HOST`: The host IP address the server listens to. Default is '127.0.0.1'.
- `PORT`: The port number the server listens on. Default is 12345.
- `TIMEOUT`: The socket timeout in seconds. Default is 5.0.
- `RECEPTION_TIMEOUT`: Timeout for the reception event in seconds. Default is 2.0.
- `SIGNAL_PORT`: Port for sending the calibration completion signal. Default is 12346.
- `REQUIRED_IMAGE_COUNT`: Number of image pairs required for stereo calibration or number of images for single calibration. Default is 20.
- `CALIBRATION_MODE`: Determines whether the server performs single or stereo calibration. Default is "STEREO". Set to "SINGLE" for single camera calibration.

## Calibration Mode Configuration

The server is designed to support both single and stereo camera calibration modes. To select the desired mode, adjust the `CALIBRATION_MODE` variable within the `TcpServer.py` script:

- Set `CALIBRATION_MODE = "SINGLE"` for single camera calibration.
- Set `CALIBRATION_MODE = "STEREO"` for stereo camera calibration.

This configuration must be done prior to starting the server for each calibration session.

## Usage

1. **Configure Calibration Mode**: Before starting the server, open `TcpServer.py` and set the `CALIBRATION_MODE` variable to either "SINGLE" or "STEREO" based on your calibration needs.

2. **Start the Server**: Run the `TcpServer.py` script to initiate the server.

    ```bash
    python TcpServer.py
    ```
    
    The server will listen for image data on the specified port.

3. **Send Image Data**: From your camera setup, send images to the server via TCP. Each image should include a header indicating its sequence, and for stereo calibration, specify left or right.

4. **Calibration Process**: After receiving the necessary number of images, the server automatically triggers the corresponding calibration script (`SingleCameraCalibration.py` or `StereoCalibration.py`). The results are saved, and a completion signal is sent back.

## Scripts

- **TcpServer.py**: Establishes a TCP server to receive images and initiates the calibration process based on the received data.

- **SingleCameraCalibration.py**: Performs calibration for a single camera. This script is invoked if the server is set to single camera mode.

- **StereoCalibration.py**: Conducts calibration for stereo cameras. This script performs individual camera calibrations and then stereo calibration, saving all relevant parameters.

- **LoadCalibrationResults.py**: Loads and displays calibration results from an `.npz` file, detailing RMS error, camera matrices, distortion coefficients, and more.

## Test Calibration with Example Images

The repository includes `LEFT` and `RIGHT` folders containing example images for stereo calibration and can be adapted for single camera calibration by placing images in a designated folder. These images are for testing and may not reflect the quality required for accurate calibration.

To test the stereo calibration:

```bash
python StereoCalibration.py
```

The script will process the example images and output the calibration results, which can then be viewed using the `LoadCalibrationResults.py` script.
For single camera calibration, ensure the script is adjusted to load images from the correct directory.

## Configuration

- Adjust `REQUIRED_IMAGE_COUNT` in `TcpServer.py` to change the number of images required for calibration.
- Modify square size and pattern settings in the respective calibration scripts as needed.

## Outputs

- Calibration parameters are stored in `stereo_calibration_parameters.npz` or a similar file for single calibration.
- Scripts output status messages to the console, providing progress updates and results.

## Viewing Calibration Results

To review the calibration results, execute:

```bash
python LoadCalibrationResults.py
```

Update the script to target the correct `.npz` file, especially if it's not located in the default directory or has a unique name.

## Troubleshooting

- Ensure the server and client share the same network and have correct IP and port configurations.
- Confirm the image format and sequence are correct when transmitting to the server.
- Monitor the console for error messages and verify that all prerequisites are correctly installed.