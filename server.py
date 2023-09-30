import websockets
import asyncio
import json
import my_llm
import time

PORT = 2023
ENGINE = "API"

# create a VideoCapture object
llm =  None if ENGINE == "API" else my_llm.get_llm() 
queryEngine = my_llm.openAI_queryEngine() if ENGINE == "API" else my_llm.get_query_engine(llm)

async def transmit(websocket, path):
    print("Client Connected !",path,'********************************************************')
    # print(query)
    try :
        query = ''
        query.strip()
        
        while True:
            query = await websocket.recv()
            print(query)

            # prompt = f"""write 50 words based on these documents.""" 

            prompt = f"""
            You are a lawyer. While writing the document STRICTLY adhere to the given metadata: {query}.
            For your client, generate an appropriate legal document based on the documents provided to be presented in the court of law.
            Choose an appropriate document template and fill in the blanks with the metadata provided.
            Be truthful, generate a highly presentable document and do not misinterpret information or invent unreasonable relationships between metadata entities.
            However, you are allowed to paraphrase the metadata GRANTED that you DO NOT add any additional metadata.
            You are also given agreementCondtions in the metadata, which contain misc stuff. 
            Use "\\n" token to symbolize the number of newlines after each paragraph.
            End this document with a disclaimer informing the client that this is an "LLM generated document" and should be used under the approval of a legal practitioner.
            """
            #             STRICTLY DO NOT modify any data in the metadata while generating the document.

            # User "\\t" token at the start of sentences to symbolize tab space wherever required.
            query.strip()
            
            # print("Query : ",query)
            
            if query == "disconnect_server":
                await websocket.send("Bye !")
                break

            # await websocket.send("test ")

            # myResponse = queryEngine.query(prompt)

            # print("Response : ",myResponse)
            # await websocket.send(myResponse)

            # -----------------------------------------------------------------
            
            myStreamResponse =queryEngine.query(prompt)
            response = ''
            for text in myStreamResponse.response_gen:
                print(text,end='')
                message = {
                    'event': 'text-generated',
                    'text': text
                }
                await websocket.send(json.dumps(message))
                await asyncio.sleep(0.1)
            
            # for i in range(20):
            #     # print(text,end='')
            #     print("Sending to client")
            #     message = {
            #         'event': 'test-somthing',
            #         'text': "testingafjas;ksijfaspfjapsifjasif"
            #     }
            #     await asyncio.sleep(0.5)
            #     await websocket.send(json.dumps(message))

                # response = response + text
                # await websocket.send('text-generated',text)
                # await websocket.send(str(text))  
            # await websocket.send(response)
            
            # -----------------------------------------------------------------
            # response_iter = llm.stream_complete(query)
            # for response in response_iter:
            #     print(response.delta, end="", flush=True)
            #     myResponse = myResponse + response.delta
            
                
    except websockets.exceptions.ConnectionClosedOK as e:
        # set authID to null when client disconnects to avoid authID conflict
        print("Client Disconnected !",path)
        
    except websockets.exceptions.ConnectionClosedError as e:
        print("Client Disconnected !",path)
    # handle 1000 error code i.e. normal closure
    except websockets.exceptions.ConnectionClosed as e:
        print("Client Disconnected !",path)

async def main():
    
    start_server = await websockets.serve(transmit, "localhost", PORT)
    print("Server Started with URL : ", start_server.server)
    print("Started server on port : ", PORT)
    await start_server.wait_closed()

asyncio.run(main())
