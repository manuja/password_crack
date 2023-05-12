# import asyncio
# import websockets

# async def hello():
#     uri = "ws://localhost:8008"
#     async with websockets.connect(uri) as websocket:
#         name = input("What's your name? ")

#         await websocket.send(name)
#         print(f">>> {name}")

#         greeting = await websocket.recv()
#         print(f"<<< {greeting}")

# if __name__ == "__main__":
#     asyncio.run(hello())
# import asyncio
# import websockets

# async def testwebsoc():
#     async with websockets.connect('ws://127.0.0.1:8002') as websocket:
#         await websocket.send("hellocc")
#         response = await websocket.recv()
#         print(response)
 
# asyncio.get_event_loop().run_until_complete(testwebsoc())

import asyncio
import websockets

# async def testwebsoc():
#     i=-1
#     win = False
#     while win == False:
        
#             i=i+1
#             print(i)
#             if(i<=2):
#              async with websockets.connect('ws://127.0.0.1:8002') as websocket:
#                 fruits = i
#                 await websocket.send(str(fruits))
#                 response = await websocket.recv()
#                 #print(response)
            
#                 print(response)
            
#             else:
#                 win=True 
# asyncio.get_event_loop().run_until_complete(testwebsoc())

async def testwebsoc():
    async with websockets.connect('ws://127.0.0.1:8002') as websocket:
                fruits = "hiii"
                await websocket.send(str(fruits))
                while True:
                    response = await websocket.recv()
                #print(response)
 
                    print(response)

asyncio.get_event_loop().run_until_complete(testwebsoc())

# import socket


# def client_program():
#     host = socket.gethostname()  # as both code is running on same pc
#     port = 8001  # socket server port number

#     client_socket = socket.socket()  # instantiate
#     client_socket.connect((host, port))  # connect to the server

#     message = "I am client sending data"  # take input

    
#     client_socket.send(message.encode())  # send message
#     data = client_socket.recv(1024).decode()  # receive response

#     print('Received from server: ' + data)  # show in terminal


#     #client_socket.close()  # close the connection


# if __name__ == '__main__':
#     client_program()