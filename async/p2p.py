import asyncio
from aioconsole import ainput

# Servers main function to constantly listen for information
async def listen(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode()
        print(f"\n> {message!r}")
    
    #print("Close connection")
    #writer.close()
    #await writer.wait_closed()
    
# Used to get input live while able to print text specifically for the client
async def live_input():
    content = await ainput("")
    return content

# Client used to send info to peer's server
async def client(): 
    while True:
        try:
            reader, writer = await asyncio.open_connection('192.168.1.48', 8888)
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
        listen, '192.168.1.60', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

async def main():
    tasks = await asyncio.gather(server(), client())
    print("\nEnd:")

asyncio.run(main())
