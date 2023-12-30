import asyncio
from aioconsole import ainput

# Servers main function to constantly listen for information
async def listen(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode()
        print(f"> {message}")
        if message == "exit":
            print("Closing server process")
            writer.close()
            await writer.wait_closed()
            break
    print("Listen end")
    

    
# Used to get input live while able to print text specifically for the client
async def live_input():
    content = await ainput("")
    return content

# Client used to send info to peer's server
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
        if msg == "exit":
            print("Closing client process")
            writer.close()
            await writer.wait_closed()
            break
    print("Client end")

# trying to do multiple tasks at same time
async def server():
    print("Server Start")
    server = await asyncio.start_server(
        listen, 'localhost', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    print("Server end")

async def main():
    tasks = await asyncio.gather(server(), client())


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
