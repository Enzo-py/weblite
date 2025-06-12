import asyncio

from utils.socket_server import ServerSocket

class Server:
    """
    Server class that handles the app.
    """

    def __init__(self):
        self.socket = ServerSocket(_print=True)

    async def run(self):
        # self.socket.on(

        # )

        async with self.socket:

        

        # while self.socket.running:
        #     await asyncio.sleep(1)
        #     # await self.socket.stop()

            # await asyncio.sleep(4)

            await self.socket.wait()

if __name__ == "__main__":
    server = Server()
    asyncio.run(server.run())