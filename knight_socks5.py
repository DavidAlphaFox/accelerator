
# copyright 2016 bjong

from struct import unpack
# import gevent
from gevent import socket, spawn
from gevent.server import StreamServer

# def to_cli(cli, serv, serv_name):
# 	try:
# 		# for buf in iter(lambda:serv.recv(1024*16), b''):
# 		# 	print(len(buf), 'from serv to cli')
# 		# 	cli.sendall(buf)
# 		[ cli.sendall(buf) for buf in iter(lambda:serv.recv(1024*16), b'') ]
# 		cli.close()
# 		serv.close()
# 	except OSError:
# 		pass
# 	print('server {} close'.format(serv_name))


def get_dst(conn):
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
		return dst
	else:
		return


def get_port(conn):
	r = conn.recv(2)
	port = unpack('>H', r)[0]
	return port


def get_dst_addr(conn):
	r = conn.recv(3)
	if r == b'\x05\x01\x00':
		conn.sendall(b'\x05\x00')
	else:
		return

	dst = get_dst(conn)
	port = get_port(conn)
	print(dst, port)
	return (dst, port)


def send(dst, buf, dst_type, dst_name):
	print(len(buf), end=' ')
	if dst_type == 'cli':
		print('{} -> {}'.format('serv', 'cli'))
	else:
		print('{} -> {}'.format('cli', 'serv'))
	dst.sendall(buf)


def reply(dst, src, dst_type, dst_name):
	try:
		# for buf in iter(lambda:src.recv(1024*16), b''):
		# 	dst.sendall(buf)
		[ send(dst,buf,dst_type,dst_name) for buf in iter(lambda:src.recv(1024*16), b'') ]
		dst.close()
		src.close()
	except OSError:
		pass
	print('{} close by {}'.format(dst_name, dst_type))
	


def reply_start(conn, dst_addr):
	dst, port = dst_addr
	s = socket.socket()
	s.connect( (dst, port) )
	conn.sendall(b'\x05\x00\x00\x01\x00\x00\x00\x00\x10\x10')
	to_cli = spawn(reply, s, conn, 'serv', dst)
	reply(conn, s, 'cli', dst_addr)
	# s.close()
	# conn.close()
	to_cli.kill()


def handle(conn, addr):
	dst_addr = get_dst_addr(conn)
	if dst_addr:
		pass
	else:
		conn.close()
		return

	reply_start(conn, dst_addr)

		
StreamServer(('0.0.0.0', 1081), handle).serve_forever()
