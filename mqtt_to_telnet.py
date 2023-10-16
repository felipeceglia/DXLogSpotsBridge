import asyncio, telnetlib3
import aiomqtt

TELNET_PORT = 23

telnet_clients = {}

async def mqtt():
    async with aiomqtt.Client("127.0.0.1") as client:
        async with client.messages() as messages:
            await client.subscribe("DXLOG_SPOTS")
            async for message in messages:
                print(message.payload.decode())
                for writer in telnet_clients.values():
                    writer.write(f'{message.payload.decode()}\n\r')


async def shell(reader, writer):
    telnet_clients[writer] = writer
    writer.write('DXLog UDP spots bridge.\n\r')
    inp = await reader.read(1)
    if inp:
        writer.echo(inp)
        writer.write('?\r\n')
        
        await writer.drain()
        
        #if inp == 'q':
        #    del telnet_clients[writer]
        #writer.close()

loop = asyncio.get_event_loop()
coro = telnetlib3.create_server(port=TELNET_PORT, shell=shell)
server = loop.run_until_complete(coro)
loop.create_task(mqtt())
loop.run_until_complete(server.wait_closed())
