from gevent.server import DatagramServer
from gevent import socket

def to_socks5(data, addr):
	print('recv', len(data), addr)
	if socket_list.get(addr):
		print('old', addr)
		s = socket_list[addr]
		s.sendall(data)
	else:
		s = socket.socket()
		s.connect( ('127.0.0.1', 7070) )
		socket_list[addr] = s
		s.sendall(data)
		for buf in iter(lambda:s.recv(8192*2),b''):
			print('tocli', len(buf), addr)
			udp_serv.sendto(buf, addr)
		print('close')
		del socket_list[addr]


socket_list = {}
udp_serv = DatagramServer(('0.0.0.0', 8389), to_socks5)
udp_serv.serve_forever()
