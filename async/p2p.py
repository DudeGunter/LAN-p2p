import asyncio
from aioconsole import ainput

# Echo the response and closes the connection with client after
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

async def listen(reader, writer):
    data = await reader.read(100)
    message = data.decode()

    print(f"PEER > {message!r}")
    
    #print("Close connection")
    #writer.close()
    #await writer.wait_closed()
    
async def live_input():
    content = await ainput(">")
    return content

# ADDED
async def client(): 
    while True:
        try:
            reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
            break
        except ConnectionRefusedError:
            print("Refused")
        except asyncio.TimeoutError:
            print("Timeout")
        else:
            print("Closed")
        await asyncio.sleep(2.0)

    while True:
        msg = await live_input()
        writer.write(msg.encode())
        await writer.drain()
        



# was main():, trying to do multiple tasks at same time
async def server():
    print("Server Start")
    server = await asyncio.start_server(
        listen, 'localhost', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

async def main():
    tasks = await asyncio.gather(server(), client())
    print("\nEnd:")

asyncio.run(main())
