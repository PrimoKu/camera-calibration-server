import socket
import sys
import select
import subprocess
import threading

def create_server_socket(host, port, timeout):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(timeout)
    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f'Server listening on port {port}')
    except OSError as msg:
        print(f'Bind failed. Error: {msg}')
        sys.exit()
    return server_socket

def receive_header(connection):
    header_data = b''
    while not header_data.endswith(b'\n'):
        try:
            chunk = connection.recv(1)
            if not chunk:
                print("Connection closed by client.")
                return None
            header_data += chunk
        except socket.timeout:
            print("Timeout while receiving the header.")
            return None
        except Exception as e:
            print(f"Error receiving header: {e}")
            return None
    return header_data.decode('utf-8').strip()

def receive_image(connection, length):
    buffer = b''
    while len(buffer) < length:
        try:
            to_read = length - len(buffer)
            data = connection.recv(4096 if to_read > 4096 else to_read)
            if not data:
                print("No more data received.")
                break
            buffer += data
        except socket.timeout:
            print("Socket timeout during image reception.")
            continue
        except Exception as e:
            print(f"Error receiving image data: {e}")
            break
    return buffer

def send_client_message(connection, message):
    connection.sendall(message.encode())

def save_image(image_data, prefix):
    global image_counts
    if reception_event.is_set() and image_counts[prefix] < required_image_count:
        image_counts[prefix] += 1
        filename = f"{prefix}/{prefix}_{image_counts[prefix]}.png"
        with open(filename, "wb") as image_file:
            image_file.write(image_data)
        print(f"{prefix} image {image_counts[prefix]} saved.")
    
        if all(count >= required_image_count for count in image_counts.values()):
            send_client_message(connection, "Calibrating...")
            reception_event.clear()
            trigger_calibration()
            reset_image_counts()

def process_image_data(connection, header):
    if reception_event.is_set():
        try:
            prefix, length_str = header.split("ImageData:")
            length = int(length_str)
            camera_side = prefix.replace("Sending", "")
            # print(f"Receiving {camera_side} image data of length: {length}")
            image_data = receive_image(connection, length)
            if image_data and len(image_data) == length:
                save_image(image_data, camera_side)
            else:
                print(f"Received incomplete {camera_side} image data.")
        except ValueError as e:
            print(f"Error parsing header or length: {header} | Error: {e}")

def trigger_calibration():
    print("Triggering stereo camera calibration...")
    subprocess.run(["python", "StereoCalibration.py"])

def reset_image_counts():
    global image_counts
    print("Resetting image counts and preparing for a new set of images.")
    for key in image_counts.keys():
        image_counts[key] = 0

def listen_for_calibration_complete():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_signal_socket:
            server_signal_socket.bind(('127.0.0.1', 12346))
            server_signal_socket.listen()
            conn, _ = server_signal_socket.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if data:
                        print(data.decode())
                        send_client_message(connection, "Calibrated!")
                        reception_event.set()
                        break

reception_event = threading.Event()
reception_event.set()

threading.Thread(target=listen_for_calibration_complete, daemon=True).start()

image_counts = {"LEFT": 0, "RIGHT": 0}
required_image_count = 20

server_socket = create_server_socket('127.0.0.1', 12345, 5.0)

while True:
    try:
        connection, client_address = server_socket.accept()
        print('Connected with ' + client_address[0] + ':' + str(client_address[1]))
        connection.settimeout(2.0)
    except socket.timeout:
        print("Server socket timeout. Awaiting new connection...")
        continue
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Closing server.")
        break
    except Exception as e:
        print(f"Error accepting connection: {e}")
        continue

    try:
        while True:
            if not reception_event.is_set():
                # print("Paused for calibration. Waiting for resume signal...")
                continue

            ready = select.select([connection], [], [], 5.0)
            if ready[0]:
                header = receive_header(connection)
                if header:
                    # print(f"Received header: {header}")
                    process_image_data(connection, header)
                else:
                    print("Header reception was incomplete or failed. Closing connection...")
                    break
            else:
                print("No data received. Checking again...")
    except KeyboardInterrupt:
        print("Keyboard interrupt received while connected. Closing connection.")
    except Exception as e:
        print(f"Error during session: {e}")

    connection.close()
    print("Connection closed. Awaiting new connection...")

server_socket.close()
print("Server closed.")