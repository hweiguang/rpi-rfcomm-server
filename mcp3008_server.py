from gpiozero import MCP3008
import bluetooth

pot_one = MCP3008(0)
pot_two = MCP3008(1)
pot_three = MCP3008(2)
pot_four = MCP3008(3)

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))
server_socket.listen(1)

port = server_socket.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_socket, "MCP3008 Server", service_id = uuid, service_classes = [uuid, bluetooth.SERIAL_PORT_CLASS], profiles = [bluetooth.SERIAL_PORT_PROFILE])

def wait_for_connection():
	print "Waiting for connection in RFCOMM channel %d" % port

	client_socket, client_info = server_socket.accept()
	print "Accepted connection from ", client_info
	send_data(client_socket)

def send_data(client_socket):
	while True:
		try:
			data = "%02f:%02f:%02f:%02f" % (pot_one.value, pot_two.value, pot_three.value, pot_four.value)
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
