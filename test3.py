from curses import echo
from pickle import FALSE
from flask import Flask, request, jsonify
from util_methods import register_service, get_ports_of_nodes, generate_node_id, get_higher_nodes, election,announce, ready_for_election, get_details, check_health_of_the_service,generate_shedule,read_password_file,broadcastFound,get_node_ports
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


import asyncio
import websockets
import socket
import logging, logging.handlers
import json
import os

counter = Value('i', 0)
app = Flask(__name__)

# verifying if port number and node name have been entered as command line arguments.
port_number = int(sys.argv[1])
assert port_number

node_name = sys.argv[2]
assert node_name

# saving the API logs to a file
logging.basicConfig(filename=f"logs/{node_name}.log", level=logging.INFO)
#print("saaaaaaaaaaaaaaaaaaa",logging.INFO)
url = 'http://localhost:5009/logDetails'
#print(url)
# print(node_name)
requests.post(url, json=node_name)

import logging.handlers
logger = logging.getLogger('Synchronous Logging')
http_handler = logging.handlers.HTTPHandler(
    '127.0.0.1:5009',
    '/logDetails',
    method='POST',
)
logger.addHandler(http_handler)

class myHTTPHandler(logging.handlers.HTTPHandler):
  def mapLogRecord(self,record):
    #print("record is sss",record)
    trec={'record':json.dumps(record.__dict__),'filename': json.dumps(node_name)}
    #trec={'filename': json.dumps(node_name)}
    return trec

myLogger = logging.getLogger('MTEST')
myLogger.setLevel(logging.INFO)
httpHandler = myHTTPHandler('localhost:5009',url='/logDetails',method="POST")
myLogger.addHandler(httpHandler)

# saving the API logs to a file
#logging.basicConfig(filename=f"logs/{node_name}.log", level=logging.INFO)
# url = 'http://localhost:5009/logDetails'
# print(url)
# print(node_name)
# requests.post(url, json=node_name)


# an array to capture the messages that receive from acceptors
learner_result_array = []

node_id = generate_node_id()
print(node_id)
bully = Bully(node_name, node_id, port_number)

# register service in the Service Registry
service_register_status = register_service(node_name, port_number, node_id)

async def handler(websocket, path):
        
        print('HIIIcc in in test3')
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
            reply.append("node 3")
            reply.append(valpass)
            # reply[1]=valpass
            #reply = f"{valpass}"
            #print(reply)
            
            await websocket.send(f"{reply}")

        asyncio.get_event_loop().stop()

async def testa():
    async with websockets.serve(handler, "localhost", 8003):
        await asyncio.Future()  # run forever
        #await asyncio.get_event_loop().run_forever()
   
@app.route('/startserver', methods=['GET'])
def startserver3():

    print("I am here in test3")
    return asyncio.run(testa())
    #return jsonify({'status':'ok'})

async def send_message(server_uri, message, password, termination_flag):
    async with websockets.connect(server_uri,ping_timeout=300) as websocket:
        await websocket.send(message)
        print(f"Sending message '{message}' to {server_uri}")

        while True:
            response = await websocket.recv()
            print(f"Received message from {server_uri}: {response}")

            # Check the condition within the send_message function
            if literal_eval(response)[1] == password:
                print("Paaword Fx !!!:", password)
                #broadcastFound(literal_eval(message)[0])
                termination_flag[0] = True
                return server_uri, response  # Include server_uri in the response

            if termination_flag[0]:
                # Terminate the inner loop if termination_flag is True
                break
    
# Send schedules to all the nodes
async def testwebsoc(shecu,node_name,passwords):

    ports_of_all_nodes = get_ports_of_nodes()
    node_details = get_details(ports_of_all_nodes)
    allports=get_node_ports(node_details)
    allports.remove(port_number)

    servers = []
    messages = []
    # tasks = []
    # stop_flag = False
    for allport in allports: 
       
        url = 'ws://127.0.0.1:'+str(allport+3000)
        print("socket open url is"+url)
        servers.append(url)

    # print("set of servrss",servers)
    # print("I am here ckient loop 1",shecu)
    keyval=0
    for singlesche in range(len(shecu)): 
        messages.append(shecu[keyval])
        keyval=keyval+1

    random.shuffle(servers)  # Randomly shuffle the servers list

    outer_termination_flag = [False]  # Flag to control the termination of the outer loop

    for password in passwords:
        termination_flag = [False]  # Flag to control the termination of the inner loop
        tasks = []

        while True:
            for server_uri, message in zip(servers, messages):
                task = asyncio.create_task(send_message(server_uri, message, password, termination_flag))
                tasks.append(task)

            responses = await asyncio.gather(*tasks, return_exceptions=True)

            # Shuffle the responses before processing
            random.shuffle(responses)

            # Process the shuffled responses
            inner_termination_flag = False
            for response in responses:
                if response is not None and not isinstance(response, Exception):
                    server_uri, response = response
                    print(f"Received message from {server_uri}: {response}")
                    # Do something with the response

                    # Check if the condition is met
                    if literal_eval(response)[1] == password:
                       # print("Password Found !!!:", password)
                        tasks.clear()  # Clear the previous tasks
                        termination_flag[0] = False  # Reset the termination flag for the inner loop
                        inner_termination_flag = True  # Set the flag to indicate termination of the inner loop
                        break  # Exit the inner loop and start from the beginning of the outer loop

            if inner_termination_flag:
                # Terminate the inner loop and move to the next iteration of the outer loop
                break

            if outer_termination_flag[0]:
                # Terminate the outer loop if outer_termination_flag is True
                break

        if outer_termination_flag[0]:
            # Break the outer loop if outer_termination_flag is True
            break

    print("End of password cracking")

def init(wait=True):
    

    #time.sleep(20)
    print("I am in init")
    

    # coro = testwebsoc()
    # # run the coroutine in an asyncio program
    # asyncio.run(coro) 
    ports_of_all_nodes = get_ports_of_nodes()
    node_details = get_details(ports_of_all_nodes)
    allports=get_node_ports(node_details)
    allports.remove(port_number)
    
    #allports.append(20000)
    print("All the ndees",allports)

    #create_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    coro2 = good(allports)
    asyncio.run(coro2)
    

    time.sleep(10)


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
            print('coordinator is ss', bully.coordinator)

            bully.election = True
            higher_nodes_array = get_higher_nodes(node_details, node_id)
            print('higher node array 1', higher_nodes_array)
            if len(higher_nodes_array) == 0:
                print("I am the leader")
                bully.coordinator = True
                bully.election = False
                announce(node_name)
                print('Leader is : %s' % node_name)
                print('**********End of electionsss 1**********************')

                #time.sleep(40)  
                passwords=[]
                passwords=read_password_file()  
                shecu=generate_shedule(node_name)
                #good()
                time.sleep(20)
                print("I came here before create shedule")
                coro = testwebsoc(shecu,node_name,passwords)
                # run the coroutine in an asyncio program
                asyncio.run(coro)
   
            else:
                print("Go for a election")
                election(higher_nodes_array, node_id)
            
    else:
        print('Service registration is not successful')

async def good(allports):
    print("I came here into async")
    for each_port in allports:
        create_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockport=each_port+3000
        print("soca is",sockport)
        
        destination = ("127.0.0.1", sockport)
        result = create_socket.connect_ex(destination)
        print("echport is....",each_port)
        if(result!=0):
            url = 'http://localhost:%s/startserver' % each_port
            #sendurl=str(url)
            #url = 'http://localhost:5002/startserver'
            print("url issss",url)
            timer_thread1 = threading.Timer(1, init)
            timer_thread1.start()
            data= requests.get(url)


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

#     # This API is used to getworkload details.
# @app.route('/destributeworkload', methods=['POST'])
# def workload_devide():
#     print("aaaaaAAAAAAAASSSSSSSSSS I am node 03")
#     data = request.get_json()
#     print(data)
#     print("mmmmmmmmmmmmm")
#     r=6
#     combination=(permutations(data['conarraycoordinator'], r))

#     dlinks = [] # create empty list to collect results
#     for x in combination:
#         s = str(x)
#         valpass=s.replace(', ', '').replace('(', '').replace(')', '').replace("'", '')
#         dlinks.append(valpass) # add results to the list
#     return jsonify({'response': dlinks}), 200
#     # print(combination)
#     # print("combi",combination[0])
#     # print("combi",combination[1])
#     # print("combi",combination[2])
#     # for x in combination:
#     #      s = str(x)
#     #      valpass=s.replace(', ', '').replace('(', '').replace(')', '').replace("'", '')
#     #      print("responce from node 03 is",valpass)
#     # #     #print(valpass)
#     #      #time.sleep(10)
#     #      return jsonify({'response': valpass}), 200
#          #return jsonify({'response': 'Ok'}), 200
#         #print(valpass)
#     # coordinator = data['coordinator']
#     # bully.coordinator = coordinator
#    # print('Coordinator is %s ' % coordinator)



'''
When nodes are sending the election message to the higher nodes, all the requests comes to this proxy. As the init
method needs to execute only once, it will forward exactly one request to the responseAPI. 
'''


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