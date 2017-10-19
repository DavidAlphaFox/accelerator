
# copyright 2016 bjong

from struct import unpack
import asyncio
import socket
# import gevent
# from gevent import socket, spawn
# from gevent.server import StreamServer


async def get_dst(reader_c):
    r = await reader_c.read(4)
    if r[:3] == b'\x05\x01\x00':
        if r[-1:] == b'\x01':
            r = await reader_c.read(4)
            dst = '.'.join([str(i) for i in unpack('BBBB', r)])
        elif r[-1:] == b'\x03':
            dst_length_bin = await reader_c.read(1)
            dst_length = unpack('B', dst_length_bin)[0]
            dst_bin = await reader_c.read(dst_length)
            dst = dst_bin.decode()
        else:
            return
        return dst
    else:
        return


async def get_port(reader_c):
    r = await reader_c.read(2)
    port = unpack('>H', r)[0]
    return port


async def get_dst_addr(reader_c, writer_c):
    r = await reader_c.read(3)
    if r == b'\x05\x01\x00':
        writer_c.write(b'\x05\x00')
    else:
        return

    dst = await get_dst(reader_c)
    port = await get_port(reader_c)
    # print(dst, port)
    return (dst, port)


# def send(dst, buf, dst_type, dst_name):
#     print(len(buf), end=' ')
#     if dst_type == 'cli':
#         print('{} -> {}'.format('serv', 'cli'))
#     else:
#         print('{} -> {}'.format('cli', 'serv'))
#     dst.sendall(buf)


async def reply(reader, writer, dst_name):
    # try:
    #     [ send(dst,buf,dst_type,dst_name) for buf in iter(lambda:src.recv(1024*16), b'') ]
    #     dst.close()
    #     src.close()
    # except OSError:
    #     pass
    while True:
        buf = await reader.read(2048*4)
        if not buf:
            break
        else:
            # print(buf[:200])
            writer.write(buf)
            await writer.drain()
    print('{} : close'.format(dst_name))


async def reply_start(reader_c, writer_c, dst_addr):
    dst, port = dst_addr
    # print('reply', dst, port)
    # dst_ip = await socket.getaddrinfo('ip.cn', port=80)[0][4][0]
    reader_s, writer_s = await asyncio.open_connection(dst, port=port, loop=loop)
    print('connect to', dst, port)
    # s = socket.socket()
    # s.connect( (dst, port) )
    writer_c.write(b'\x05\x00\x00\x01\x00\x00\x00\x00\x10\x10')
    await writer_s.drain()
    loop.create_task(reply(reader_c, writer_s, dst))
    await reply(reader_s, writer_c, dst_addr)
    # to_cli.kill()


async def handle(reader_c, writer_c):
    # reader_s, writer_s = await asyncio.open_connection('ip.cn', 80, loop=loop)
    # exit()


    dst_addr = await get_dst_addr(reader_c, writer_c)
    if dst_addr:
        # print(dst_addr)
        pass
    else:
        # reader_c.close()
        return

    await reply_start(reader_c, writer_c, dst_addr)


ip, port = '127.0.0.1', 1080
loop = asyncio.get_event_loop()
core = asyncio.start_server(handle, ip, port, loop=loop)
server = loop.run_until_complete(core)
loop.run_forever()
