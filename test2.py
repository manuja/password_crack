from curses import echo
from flask import Flask, request, jsonify
from util_methods import register_service, get_ports_of_nodes, generate_node_id, get_higher_nodes, election,announce, ready_for_election, get_details, check_health_of_the_service,generate_shedule
from bully import Bully
import threading
import time
import random
import sys
import requests
from multiprocessing import Value
import logging
from itertools import combinations
from itertools import permutations
import asyncio
import websockets
import socket
import json
import numpy as np
from ast import literal_eval
#from server import handler

counter = Value('i', 0)
app = Flask(__name__)

# verifying if port number and node name have been entered as command line arguments.
port_number = int(sys.argv[1])
assert port_number

node_name = sys.argv[2]
assert node_name

# saving the API logs to a file
logging.basicConfig(filename=f"logs/{node_name}.log", level=logging.INFO)

# an array to capture the messages that receive from acceptors
learner_result_array = []

node_id = generate_node_id()
print(node_id);
bully = Bully(node_name, node_id, port_number)

# register service in the Service Registry
service_register_status = register_service(node_name, port_number, node_id)

async def handler(websocket, path):
        
        print('HIIIcc')
        fruits = ["apple", "banana", "cherry"]
        data = await websocket.recv()
        r=6
        combination=(permutations(data, r))

        for x in combination:
            #time.sleep(4)
            s = str(x)
            valpass=s.replace(', ', '').replace('(', '').replace(')', '').replace("'", '')
            reply=[]
            #print("node name is ...................................", bully.node_name)
            reply.append("node 2")
            reply.append(valpass)
            # reply[1]=valpass
            #reply = f"{valpass}"
            #print(reply)
            
            await websocket.send(f"{reply}")

        asyncio.get_event_loop().stop()

      


async def testa():
    async with websockets.serve(handler, "localhost", 8002):
        await asyncio.Future()  # run forever
        #await asyncio.get_event_loop().run_forever()
   

def startserver():

    print("I am here in test2")
    asyncio.run(testa())
    

  

     

    # start_server = websockets.serve(handler, "localhost", 8002)
    
    # asyncio.get_event_loop().run_until_complete(start_server)
    
    # asyncio.get_event_loop().run_forever()  
    



# async def handler(websocket, path):
 
#     data = await websocket.recv()

#     #ports_of_all_nodes = get_ports_of_nodes()
 
#     reply = f"Data recieved as mmmmmm:  {data}!"
 
#     await websocket.send(reply)


# async def handler(websocket, path):
 
#     data = await websocket.recv()
#     print(data)
#     # itrdata=int(data)
#     # #ports_of_all_nodes = get_ports_of_nodes()
#     # fruits = ["apple", "banana", "cherry"]
#     # #for x in fruits:
#     # datax=fruits[itrdata]
#     reply = f"Data recieved as mmmmmm:  {data}!"
#     await websocket.send(reply) 




#  # create the custom coroutine
# coro = handler(websocket, path)
# # run the coroutine in an asyncio program
# asyncio.run(coro)

def init(wait=True):

    
    # start_server = websockets.serve(handler, "localhost", 8002)
 
    # asyncio.get_event_loop().run_until_complete(start_server)
 
    # asyncio.get_event_loop().run_forever()

    if service_register_status == 200:
        ports_of_all_nodes = get_ports_of_nodes()
        del ports_of_all_nodes[node_name]

        # exchange node details with each node
        node_details = get_details(ports_of_all_nodes)

        if wait:
            timeout = random.randint(5, 15)
            time.sleep(timeout)
            print('timeouting in %s seconds' % timeout)

        # checks if there is an election on going
        election_ready = ready_for_election(ports_of_all_nodes, bully.election, bully.coordinator)
        if election_ready or not wait:
            print('Starting election in: %s' % node_name)
            bully.election = True
            higher_nodes_array = get_higher_nodes(node_details, node_id)
            print('higher node array', higher_nodes_array)
            if len(higher_nodes_array) == 0:
                bully.coordinator = True
                bully.election = False
                announce(node_name)
                print('Leader is : %s' % node_name)
                print('**********End of election**********************')
                generate_shedule(node_name)
                
            else:
                election(higher_nodes_array, node_id)
    else:
        print('Service registration is not successful')


# this api is used to exchange details with each node
@app.route('/nodeDetails', methods=['GET'])
def get_node_details():
    coordinator_bully = bully.coordinator
    node_id_bully = bully.node_id
    election_bully = bully.election
    node_name_bully = bully.node_name
    port_number_bully = bully.port
    return jsonify({'node_name': node_name_bully, 'node_id': node_id_bully, 'coordinator': coordinator_bully,
                    'election': election_bully, 'port': port_number_bully}), 200


'''
This API checks if the incoming node ID is grater than its own ID. If it is, it executes the init method and 
sends an OK message to the sender. The execution is handed over to the current node. 
'''

# def getpassword():

#     from server import Server

#     return Server.startser()

    # start_server = websockets.serve(handler, "localhost", 8002)
    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()


 
# start_server = websockets.serve(handler, "localhost", 8002)
 
 
# asyncio.get_event_loop().run_until_complete(start_server)
 
# asyncio.get_event_loop().run_forever()

@app.route('/response', methods=['POST'])
def response_node():
    data = request.get_json()
    incoming_node_id = data['node_id']
    self_node_id = bully.node_id
    if self_node_id > incoming_node_id:
        threading.Thread(target=init, args=[False]).start()
        bully.election = False
    return jsonify({'Response': 'OK'}), 200


# This API is used to announce the coordinator details.
@app.route('/announce', methods=['POST'])
def announce_coordinator():
    data = request.get_json()
    coordinator = data['coordinator']
    bully.coordinator = coordinator
    print('Coordinator is %s ' % coordinator)
    return jsonify({'response': 'OK'}), 200

# This API is used to announce the password found details.
@app.route('/announce_found', methods=['POST'])
def announce_found():
    data = request.get_json()
    message = data['message']
    print('Password have been cracked by %s ' % message)
    return jsonify({'response': 'OK'}), 200

# This API is used to getworkload details.
@app.route('/destributeworkload', methods=['POST'])
def workload_devide():
   # print("aaaaaAAAAAAAASSSSSSSSSS I am node 02")
    data = request.get_json()

    dictionary = data
    jsonString = json.dumps(dictionary, indent=4)
   #print("sasasasasas",jsonString)

    python_obj = json.loads(jsonString)

    owned_array = python_obj['conarraycoordinator']
    nodeis = python_obj['nodename']
    # print(python_obj['conarraycoordinator']) 
    # print(nodeis)
    # print("mmmmmmmmmmmmm")
    # r=6
    # combination=(permutations(data['conarraycoordinator'], r))
    #shecu = data['conarraycoordinator']
    #node_nameof = data['node_name']

    coro = testwebsoc(owned_array,nodeis)
    # run the coroutine in an asyncio program
    asyncio.run(coro) 

    return jsonify({'response': "ok"}), 200

async def testwebsoc(shedcu,node_name):
   # print("hii")
    #json.loads(shedcu)
   # echo("owned array is",shedcu)
    # all_nodes=[]
    # all_nodes = get_ports_of_nodes()
    # print("current all nodes",all_nodes);
    # print("need to remove id",node_name);
    # all_nodes.pop(node_name)
    # print("after remove id",all_nodes);

    # #url = 'ws://127.0.0.1:%s/getpassword' % (all_nodes[each_node]+3000)
    port="8002"
    #url = 'ws://127.0.0.1:%s/' % (port)
    url = 'ws://127.0.0.1:8002'
    print(url)

    async with websockets.connect(url) as websocket:
            schedule = shedcu
            indica=True
            await websocket.send(schedule)
            while True:
                response = await websocket.recv()
                #print(response)
                #jsonString = json.dumps(dictionary, indent=4)
                #print("sasasasasas",jsonString)
                print(response)
                    #if(response==""):
                    #     print("samaaaaaaaaaaaaaaaaaaaa")

                    #     start_server = websockets.serve(Test2.handler, "localhost", 8002)

                    #     Test2.asyncio.get_event_loop().run_until_complete(start_server)

                    #     Test2.asyncio.get_event_loop().run_forever()

                    # else:
                    #     print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
                           
           
             
            #     print(response)

# async def handler(websocket, path):
    
#     print('HIIIcc')
#     fruits = ["apple", "banana", "cherry"]
#     data = await websocket.recv()
#     #print(data)
#     #itrdata=int(data)
#     #ports_of_all_nodes = get_ports_of_nodes()
#     #for x in fruits:
#     #datax=fruits[itrdata]
#     for i in range(15) :
#         reply = f"Data recieved as mmmmmm:  {data}!"
#         await websocket.send(reply)
 
# start_server = websockets.serve(handler, "localhost", 8002)
 
 
# asyncio.get_event_loop().run_until_complete(start_server)
 
# asyncio.get_event_loop().run_forever()


@app.route('/proxy', methods=['POST'])
def proxy():
    with counter.get_lock():
        counter.value += 1
        unique_count = counter.value

    url = 'http://localhost:%s/response' % port_number
    if unique_count == 1:
        data = request.get_json()
        requests.post(url, json=data)

    return jsonify({'Response': 'OK'}), 200


# No node spends idle time, they always checks if the master node is alive in each 60 seconds.
def check_coordinator_health():
    threading.Timer(60.0, check_coordinator_health).start()
    health = check_health_of_the_service(bully.coordinator)
    if health == 'crashed':
        init()
    else:
        print('Coordinator is alive')


 
 



timer_thread1 = threading.Timer(15, init)
timer_thread1.start()

# timer_thread2 = threading.Timer(60, check_coordinator_health)
# timer_thread2.start()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port_number)