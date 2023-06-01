from flask import Flask, render_template, request
import socket
import struct
from pymodbus.utilities import computeCRC

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def read_data():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 6000

    slave_id = int(request.form['slave_id'])
    function_code = int(request.form['function_code'])
    starting_address = int(request.form['starting_address'])
    quantity = int(request.form['quantity'])

    message = bytearray([slave_id, function_code, starting_address >> 8, starting_address & 0xff, quantity >> 8, quantity & 0xff])
    crc = computeCRC(message)
    message += crc.to_bytes(2, byteorder='big')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))

    sock.send(message)

    response = sock.recv(1024)

    data = response[3:]
    values = [int.from_bytes(data[i:i+2], byteorder='big') for i in range(0, len(data), 2)]

    sock.close()

    data_list = []
    i = 0
    while i < len(values):
        address = starting_address + i
        value1 = hex(values[i])
        value2 = hex(values[i+1]) if i+1 < len(values) else None
        combined_value = (values[i] << 16) + values[i+1] if i+1 < len(values) else values[i] << 16

        # Convert to IEEE 754 (Floating Point)
        binary_value = struct.pack('>I', combined_value)
        ieee754_value = struct.unpack('>f', binary_value)[0]

        i += 2

        data_list.append({
            'address': address,
            'value1': value1,
            'value2': value2,
            'combined_value': hex(combined_value),
            'ieee754_value': ieee754_value
        })

    return render_template('index.html', data_list=data_list)

if __name__ == '__main__':
    app.run(debug=True)
