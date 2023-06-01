import socket
from pymodbus.utilities import computeCRC
import struct

TCP_IP = '127.0.0.1'
TCP_PORT = 6000

slave_id = input("Enter slave id: ")
function_code = input("Enter function code: ")
starting_address = input("Enter starting address: ")
quantity =  input("Enter quantity: ")

starting_address = int(starting_address)
quantity = int(quantity)
slave_id = int(slave_id)
function_code = int(function_code)


message = bytearray([slave_id, function_code, starting_address >>
                    8, starting_address & 0xff, quantity >> 8, quantity & 0xff])

crc = computeCRC(message)

message += crc.to_bytes(2, byteorder='big')

print(message)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

sock.send(message)

response = sock.recv(1024)

data = response[3:]
values = [int.from_bytes(data[i:i+2], byteorder='big')
          for i in range(0, len(data), 2)]

binary_values = [bin(value)[2:].zfill(16) for value in values]

# convert binary string to float
float_values = []
for binary_string in binary_values:
    little_endian = binary_string[8:] + binary_string[:8]  # change from Big Endian to Little Endian
    f = struct.unpack('<f', bytes.fromhex('%08x' % int(little_endian, 2)))[0]  # unpack as Little Endian float
    float_values.append(f)

print("Data (Decimal): ", values)
print("Data (Binary): ", binary_values)
print("Data (Floating Point): ", float_values)

sock.close()
