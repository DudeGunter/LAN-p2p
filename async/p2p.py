import asyncio

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()

# ADDED
async def client():
    while True:
        print("A")
        await asyncio.sleep(1)

# was main():, trying to do multiple tasks at same time
async def server():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

async def main():
    print("Start: \n")
    tasks = await asyncio.gather(server(), client())
    print("\nEnd:")
asyncio.run(main())