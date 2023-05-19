from pickle import FALSE
from flask import Flask, request, jsonify
from util_methods import register_service, get_ports_of_nodes, generate_node_id, get_higher_nodes, election, announce, ready_for_election, get_details, check_health_of_the_service, generate_shedule,workloaddevide,read_password_file,broadcastFound
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
#from test2 import startserver 
from ast import literal_eval

import asyncio
import websockets
import socket
import logging, logging.handlers
import json

counter = Value('i', 0)
app = Flask(__name__)

#startserver()


# verifying if port number and node name have been entered as command line arguments.
port_number = int(sys.argv[1])
assert port_number

node_name = sys.argv[2]
assert node_name

# saving the API logs to a file
#logging.basicConfig(filename=f"logs/{node_name}.log", level=logging.INFO)
# print("saaaaaaaaaaaaaaaaaaa",logging.INFO)
# url = 'http://localhost:5009/logDetails'
# print(url)
# # print(node_name)
# requests.post(url, json=node_name)

# # Import logging.handlers module
# import logging.handlers
# # Create the demo handler
# demoHandler = logging.handlers.HTTPHandler('http://localhost:5009/logDetails', '', method= 'POST')
# logger = logging.getLogger()
# # Add the handler we created
# log = logger.addHandler(demoHandler)
# # Emit a log message
# logger.warning("Warning Message!")

# import logging.handlers
# logger = logging.getLogger('Synchronous Logging')
# http_handler = logging.handlers.HTTPHandler(
#     '127.0.0.1:5009',
#     '/logDetails',
#     method='POST',
# )
# logger.addHandler(http_handler)

# Log messages:
# logger.warn('Hey log a warning')
# logger.error("Hey log a error")

#logging.basicConfig(filename=f"logs/{node_name}.log", level=logging.INFO)



class myHTTPHandler(logging.handlers.HTTPHandler):
  def mapLogRecord(self,record):
    print("record is sss",record)
    trec={'record':json.dumps(record.__dict__),'filename': json.dumps(node_name)}
    #trec={'filename': json.dumps(node_name)}
    return trec

# myLogger = logging.getLogger('MTEST')
# myLogger.setLevel(logging.INFO)
# httpHandler = myHTTPHandler('localhost:5009',url='/logDetails',method="POST")
# myLogger.addHandler(httpHandler)

# myLogger.info('Small info message')
# myLogger.debug('Small debug message')
# myLogger.error('Small error message')





# an array to capture the messages that receive from acceptors
learner_result_array = []

node_id = generate_node_id()
print(node_id);
bully = Bully(node_name, node_id, port_number)

# register service in the Service Registry
service_register_status = register_service(node_name, port_number, node_id)

print("SRS",service_register_status)

#open the port
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
    async with websockets.serve(handler, "localhost", 8003):
        await asyncio.Future()  # run forever
        #await asyncio.get_event_loop().run_forever()
   

def startserver1():

    print("I am here in test3")
    asyncio.run(testa())

# def startse():
#     print("okkkk")
#     startserver()
    
 
async def testwebsoc(shecu,node_name,passwords):

    print("I am here ckient loop")
    #startserver()
  
    port="8002"
    url = 'ws://127.0.0.1:8002'
    print(url)
    print("set of password is",passwords)
    keyval=0
    for passval in range(len(passwords)):
        print("I started the next loop")
        time.sleep(10)
        passwords_value= passwords[keyval]
        async with websockets.connect(url) as websocket:
            schedule = shecu
            print("asddd",schedule[0])
            indica=True
            await websocket.send(schedule[0])
            indi=True
            
            
            while indi==True:
                
                response = await websocket.recv()
                #print(response)
                #jsonString = json.dumps(dictionary, indent=4)
                #print("sasasasasas",jsonString)
                print(literal_eval(response)[1])
                if (literal_eval(response)[1]) == passwords_value:
                    keyval=keyval+1
                    print("Password Has Found !!!!")
                    print("Password Has Found By ",literal_eval(response)[0],"!!!!!!")
                    broadcastFound(literal_eval(response)[0])
                    #asyncio.get_event_loop().stop()
                    indi=FALSE
                    break
                else:
                    print("Password Doesnot matched")
                # if response=="2C1Dbd" :
                #     print("Foundddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
                    ###########asyncio.get_event_loop().stop()
                # if(response==""):
                #     indi=False
            #asyncio.get_event_loop().stop()    
    print("Exit the password matching process !!!")

#startserver()    

def init(wait=True):
    


    print("I am in init")
    passwords=[]
    passwords=read_password_file()
    create_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destination = ("127.0.0.1", 8002)

    

    result = create_socket.connect_ex(destination)
    if result != 0:
        from test2 import startserver 
        
        myLogger = logging.getLogger('MTEST')
        myLogger.setLevel(logging.DEBUG)
        httpHandler = myHTTPHandler('localhost:5009',url='/logDetails',method="POST")
        myLogger.addHandler(httpHandler)
        myLogger.info('Web socket started')
        
        startserver()
        print("Port is not open")
        

   
    
    #startse()
   ## startserver()
    # corot = startse()
    # # run the coroutine in an asyncio program
    # asyncio.run(corot)
    

    # coro = testwebsoc()
    # # run the coroutine in an asyncio program
    # asyncio.run(coro) 
    




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
                print('**********End of electionsss**********************')
                
                #########################
                # async with websockets.connect('ws://127.0.0.1:8000') as websocket:
                #     await websocket.send("helloccmmmm")
                #     response = await websocket.recv()
                #     print(response)
                #testwebsoc(node_id)
                #shedcu ={}
                shecu=generate_shedule(node_name)
                print("print array is",shecu)
                #shedcu = shedcu[0]
                #node_id = "56"
                #testwebsoc()
                # create the custom coroutine
                # coro = testwebsoc()
          
          
          
          
          
          
          
          
          
          
          
                # # run the coroutine in an asyncio program
                # asyncio.run(coro)
                print("aaasamaaaaaaaaaaaaaaaaaaaa")

                
                # retval=startserver()
                # print(retval)

                print("I came here")
                coro = testwebsoc(shecu,node_name,passwords)
                # run the coroutine in an asyncio program
                asyncio.run(coro) 
                

                #Distribute the shcedule to the nodes
                ########################workloaddevide(shecu,node_name)

               
                
            else:
                election(higher_nodes_array, node_id)
            
    else:
        print('Service registration is not successful')


# async def hello():
#     uri = "ws://localhost:8008"
#     async with websockets.connect(uri) as websocket:
#         name = input("What's your name? ")

#         await websocket.send(name)
#         print(f">>> {name}")

#         greeting = await websocket.recv()
#         print(f"<<< {greeting}")  
    

# async def testwebsoc():
#     abc="hiiii"
#     response={}
#     print(":::::::::::::::::",)
#     #shecu=generate_shedule(node_name)
    
#     print(":::::::::::::::::",)
#     async with websockets.connect('ws://127.0.0.1:8001') as websocket:
#         await websocket.send(abc)
#         response = await websocket.recv()
#         print(response)
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

# start_server = websockets.serve(handler, "localhost", 8002)


# asyncio.get_event_loop().run_until_complete(start_server)

# asyncio.get_event_loop().run_forever()

# async def testwebsoc(shedcu,node_name):

    

#     print("combined array is",shedcu)
#     all_nodes=[]
#     all_nodes = get_ports_of_nodes()
#     print("current all nodes",all_nodes);
#     print("need to remove id",node_name);
#     all_nodes.pop(node_name)
#     print("after remove id",all_nodes);

    ##############################################

    # start_server = websockets.serve(handler, "localhost", 8002)


    # asyncio.get_event_loop().run_until_complete(start_server)

    # asyncio.get_event_loop().run_forever()


    ##############################################
    # if(len(all_nodes)>=1):
    #     print("samaaaaaaaaaaaaaaaaaaaa")

    #     start_server = websockets.serve(Test2.handler, "localhost", 8002)

    #     Test2.asyncio.get_event_loop().run_until_complete(start_server)

    #     Test2.asyncio.get_event_loop().run_forever()

    # else:
    #     print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")



    # incre=0
    # for each_node in all_nodes:

    #     data = {
    #      'conarraycoordinator': shedcu[incre].tolist()
    #     }
        

    #     #url = 'ws://127.0.0.1:%s/getpassword' % (all_nodes[each_node]+3000)
    #     url = 'ws://127.0.0.1:%s/' % (all_nodes[each_node]+3000)
    #     print(url)

        

        # async def testwebsoc():
        #         async with websockets.connect(url) as websocket:
        #             fruits = "hiii"
        #             await websocket.send(str(fruits))
        #             while True:
        #                 response = await websocket.recv()
        #             #print(response)
 
        #                 print(response)
        





    ###############################################
    # i=-1
    # win = False
    # while win == False:
        
    #         i=i+1
    #         print(i)
    #         if(i<=2):
    #          async with websockets.connect('ws://127.0.0.1:8001') as websocket:
    #             fruits = shedcu[i]
    #             await websocket.send(str(fruits))
    #             response = await websocket.recv()
    #             #print(response)
            
    #             print(response)
            
    #         else:
    #             win=True 
 
#asyncio.get_event_loop().run_until_complete(testwebsoc())
#for x in range(3):
# coro = testwebsoc()
#                 # run the coroutine in an asyncio program
# asyncio.run(coro) 

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
    print(data)
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
    print("aaaaaAAAAAAAASSSSSSSSSS I am node 01")
    data = request.get_json()
    print(data)
    print("mmmmmmmmmmmmm")
    r=6
    combination=(permutations(data['conarraycoordinator'], r))

    # print(combination)
    # print("combi",combination[0])
    # print("combi",combination[1])
    # print("combi",combination[2])

    # for x in combination:
    #      s = str(x)
    #      valpass=s.replace(', ', '').replace('(', '').replace(')', '').replace("'", '')
    #      #print("responce from node 01 is",valpass)
    # #     #print(valpass)
    #      #time.sleep(10)
    #      return jsonify({'response': valpass}), 200
    dlinks = [] # create empty list to collect results
    for x in combination:
        s = str(x)
        valpass=s.replace(', ', '').replace('(', '').replace(')', '').replace("'", '')
        dlinks.append(valpass) # add results to the list
    return jsonify({'response': dlinks}), 200
    #return dlinks 
    
    #for x in combination:
        # s = str(x)
        # valpass=s.replace(', ', '').replace('(', '').replace(')', '').replace("'", '')
         #print("responce from node 01 is",valpass)
         #time.sleep(10)
        # yield [(value[0], key) for key, value in combination]
         #return jsonify({'response': valpass}), 200
         #return jsonify({'response': 'Ok'}), 200
        #print(valpass)
    # coordinator = data['coordinator']
    # bully.coordinator = coordinator
   # print('Coordinator is %s ' % coordinator)
    

'''
When nodes are sending the election message to the higher nodes, all the requests comes to this proxy. As the init
method needs to execute only once, it will forward exactly one request to the responseAPI. 
'''


@app.route('/proxy', methods=['POST'])
def proxy():
    print("Yes I am here no worries")
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
    # else:
    #     print('Coordinator is alive')





timer_thread1 = threading.Timer(15, init)
timer_thread1.start()

# timer_thread2 = threading.Timer(60, check_coordinator_health)
# timer_thread2.start()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port_number)