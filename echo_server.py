import bluetooth

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))
server_socket.listen(1)

port = server_socket.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_socket, "Echo Server", service_id = uuid, service_classes = [uuid, bluetooth.SERIAL_PORT_CLASS], profiles = [bluetooth.SERIAL_PORT_PROFILE])

def wait_for_connection():
	print "Waiting for connection in RFCOMM channel %d" % port

	client_socket, client_info = server_socket.accept()
	print "Accepted connection from ", client_info
	listen_for_data(client_socket)

def listen_for_data(client_socket):
	while True:
		try:
			data = client_socket.recv(1024)
			print "Received: %s" % data
			client_socket.send(data)

		except IOError:
			print "Client has disconnected"
			wait_for_connection()
			break

		except KeyboardInterrupt:
			print "Shutting down socket"
			server_socket.close()
			client_socket.close()

wait_for_connection()
