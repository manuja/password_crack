import random
import asyncio
import websockets
from ast import literal_eval

async def send_message(server_uri, message, password, termination_flag):
    async with websockets.connect(server_uri,ping_timeout=300) as websocket:
        await websocket.send(message)
        print(f"Sending message '{message}' to {server_uri}")

        while True:
            response = await websocket.recv()
            print(f"Received message from {server_uri}: {response}")

            # Check the condition within the send_message function
            if literal_eval(response)[1] == password:
                print("Paaword F !!!:", password)
                termination_flag[0] = True
                return server_uri, response  # Include server_uri in the response

            if termination_flag[0]:
                # Terminate the inner loop if termination_flag is True
                break



async def main():
    servers = ["ws://127.0.0.1:8002", "ws://127.0.0.1:8003"]
    messages = [['0', '1', 'a', 'b', 'A', 'B'], ['2', '3', 'c', 'd', 'C', 'D']]
    passwords = ["01aBbA", "23cDdD"]

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

    # Rest of the code

asyncio.run(main())
