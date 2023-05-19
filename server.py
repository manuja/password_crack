# import asyncio
# import websockets
# import logging

# async def hello(websocket):
#     name = await websocket.recv()
#     print(f"<<< {name}")

#     greeting = f"Hello {name}!"

#     await websocket.send(greeting)
#     print(f">>> {greeting}")

# async def main():
#     async with websockets.serve(hello, "localhost", 8008):
#         logging.basicConfig( #Added by me in order to debug
#             format="%(message)s",
#             level=logging.DEBUG, 
#         )
#         await asyncio.Future()  # run forever

# if __name__ == "__main__":
#     asyncio.run(main())





import asyncio
 
import websockets

from itertools import combinations
from itertools import permutations
import json
import time 
from util_methods import register_service, get_ports_of_nodes, generate_node_id, get_higher_nodes, election, announce, ready_for_election, get_details, check_health_of_the_service, generate_shedule
 
# create handler for each connection
 
# async def handler(websocket, path):
    
#     print('HIIIcc')
#     fruits = ["apple", "banana", "cherry"]
#     data = await websocket.recv()
#     r=6
#     combination=(permutations(data, r))

#     for x in combination:
#         time.sleep(4)
#         s = str(x)
#         valpass=s.replace(', ', '').replace('(', '').replace(')', '').replace("'", '')
#         reply = f"{valpass}"
         
        
#         await websocket.send(reply)
        
 
# start_server = websockets.serve(handler, "localhost", 8002)
 
# asyncio.get_event_loop().run_until_complete(start_server)
 
# asyncio.get_event_loop().run_forever()



async def handler(websocket, path):
        
        print('HIIIcc')
        fruits = ["apple", "banana", "cherry"]
        data = await websocket.recv()
        r=6
        #combination=(permutations(data, r))

        for x in fruits:
            #time.sleep(4)
            s = str(x)
            valpass=s.replace(', ', '').replace('(', '').replace(')', '').replace("'", '')
            reply = f"{valpass}"
            
            
            await websocket.send(reply)

        #asyncio.get_event_loop().stop()


async def testa():
    async with websockets.serve(handler, "localhost", 8003):
        await asyncio.Future()  # run forever


asyncio.run(testa())

# async def handler(websocket, path):
    
#     fruits = ["apple", "banana", "cherry"]
#     data = await websocket.recv()
#     reply = f"Data recieved as mmmmmm:  {data}!"
#     indi=False
#     x=0
#     while(indi==False):
#         #print(data)
#         for x in range(5) :
#             print(x)
#             await websocket.send(str(x))
 
# start_server = websockets.serve(handler, "localhost", 8002)

# asyncio.get_event_loop().run_until_complete(start_server)
 
# asyncio.get_event_loop().run_forever()

# class Server:
 
#  async def handler(websocket, path):
 
#     data = await websocket.recv()
#     print(data)
#     # itrdata=int(data)
#     # #ports_of_all_nodes = get_ports_of_nodes()
#     # fruits = ["apple", "banana", "cherry"]
#     # #for x in fruits:
#     # datax=fruits[itrdata]
#     reply = f"Data recieved as mmmmmm:  {data}!"
#     await websocket.send(reply)
 
#  async def startser():
 
#     start_server = websockets.serve(Server.handler, "localhost", 8002)
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()

# import socket


# def server_program():
#     # get the hostname
#     host = socket.gethostname()
#     port = 8001  # initiate port no above 1024

#     server_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     server_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     server_socket.listen(2)
#     conn, address = server_socket.accept()  # accept new connection
#     print("Connection from: " + str(address))
#     while True:
#         # receive data stream. it won't accept data packet greater than 1024 bytes
#         data = conn.recv(1024).decode()
#         if not data:
#             # if data is not received break
#             break
#         print("from connected user: " + str(data))
#         data = "I am server sending data"
#         conn.send(data.encode())  # send data to the client

#     #conn.close()  # close the connection

# if __name__ == '__main__':
#     server_program()