
# copyright 2016 bjong

from struct import unpack
# import gevent
from gevent import socket, spawn
from gevent.server import StreamServer

def to_cli(cli, serv, serv_name):
	try:
		for buf in iter(lambda:serv.recv(1024*16), b''):
			print(len(buf), 'from serv to cli')
			cli.sendall(buf)
	except OSError:
		pass
	cli.close()
	serv.close()
	print('server {} close'.format(serv_name))


def handle(conn, addr):
	r = conn.recv(3)
	if r == b'\x05\x01\x00':
		conn.sendall(b'\x05\x00')
	else:
		return

	r = conn.recv(4)
	if r[:3] == b'\x05\x01\x00':
		if r[-1:] == b'\x01':
			r = conn.recv(4)
			dst = '.'.join([str(i) for i in unpack('BBBB', r)])
		elif r[-1:] == b'\x03':
			dst_length = unpack('B', conn.recv(1))[0]
			dst = conn.recv(dst_length).decode()
		else:
			return
		r = conn.recv(2)
		port = unpack('>H', r)[0]
		print(dst, port)
		
		s = socket.socket()
		s.connect( (dst, port) )
		g = spawn(to_cli, conn, s, dst)
		g.start()
		conn.sendall(b'\x05\x00\x00\x01\x00\x00\x00\x00\x10\x10')
		try:
			for buf in iter(lambda:conn.recv(1024*16), b''):
				print(len(buf), 'from cli to serv ', buf)
				s.sendall(buf)
		except OSError:
			pass
		s.close()
		conn.close()
		g.kill()
	else:
		return


StreamServer(('0.0.0.0', 1081), handle).serve_forever()
