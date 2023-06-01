import socket
from pymodbus.utilities import computeCRC
import time
import sys
import tkinter as tk
from tkinter import ttk
import pandas as pd

TCP_IP = '127.0.0.1'
TCP_PORT = 6000


def send_modbus_request():
    slave_id = int(slave_id_entry.get())
    function_code = int(function_code_entry.get())
    starting_address = int(starting_address_entry.get())
    quantity = int(quantity_entry.get())

    message = bytearray([slave_id, function_code, starting_address >>
                        8, starting_address & 0xff, quantity >> 8, quantity & 0xff])
    crc = computeCRC(message)
    message += crc.to_bytes(2, byteorder='big')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))

    sock.send(message)

    response = sock.recv(1024)

    data = response[3:]
    values = [int.from_bytes(data[i:i+2], byteorder='big')
              for i in range(0, len(data), 2)]

    sock.close()

    # clear table data
    data_table.delete(*data_table.get_children())

    # insert data with index
    count = 0
    for value in values:
        address = starting_address + count
        data_table.insert(parent='', index=count, values=(address, value))
        count += 1

    # continue reading until stop button is pressed
    root.after(1000, send_modbus_request)


def clear_data():
    data_table.delete(*data_table.get_children())

root = tk.Tk()
root.title('Modbus Client')
root.configure(bg='#F0F0F0')

slave_id_label = tk.Label(root, text='Slave ID:', font='Helvetica 10 bold')
slave_id_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
slave_id_entry = tk.Entry(root, width=50)
slave_id_entry.grid(row=0, column=1,padx=5, pady=5, sticky='w')

function_code_label = tk.Label(
root, text='Function Code:', font='Helvetica 10 bold')
function_code_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
function_code_entry = tk.Entry(root, width=50)
function_code_entry.grid(row=1, column=1,padx=5, pady=5, sticky='w')

starting_address_label = tk.Label(
root, text='Starting Address:', font='Helvetica 10 bold')
starting_address_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
starting_address_entry = tk.Entry(root, width=50)
starting_address_entry.grid(row=2, column=1,padx=5, pady=5, sticky='w')

quantity_label = tk.Label(
root, text='Quantity:', font='Helvetica 10 bold')
quantity_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
quantity_entry = tk.Entry(root, width=50)
quantity_entry.grid(row=3, column=1,padx=5, pady=5, sticky='w')



data_table_frame = tk.Frame(root)
data_table_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
data_table = ttk.Treeview(data_table_frame, columns=('address', 'value'), show='headings',)
data_table.grid(row=0, column=0, sticky='nsew')
data_table.heading('address', text='Address')
data_table.column('address', width=100)
data_table.heading('value', text='Value')
data_table.column('value', width=100)
data_table_frame.columnconfigure(0, weight=1)
data_table_frame.rowconfigure(0, weight=1)


button_frame = tk.Frame(root)
button_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
start_button = tk.Button(button_frame, text='Start Reading', command=send_modbus_request, bg='#00FF00')
start_button.pack(side=tk.LEFT, padx=5, pady=5)
clear_button = tk.Button(button_frame, text='Clear Data', command=clear_data, bg='#FF0000')
clear_button.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()


