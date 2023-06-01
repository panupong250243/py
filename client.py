import socket
from pymodbus.utilities import computeCRC

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

value = int.from_bytes(data[0:2], byteorder='big')

sock.close()

data = response[3:]
values = [int.from_bytes(data[i:i+2], byteorder='big')
          for i in range(0, len(data), 2)]
print("Data: ", values)
