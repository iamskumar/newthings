from flask import Flask, request
import asyncio
import json
import websocket
import websockets

app = Flask(__name__)


@app.route('/send_message', methods=['POST'])
async def send_message(bet):
    #bet = request.form['bet']
    async with websockets.connect('ws://western-lavish-barracuda.glitch.me/:5000') as websocket:
        await websocket.send(bet)
        response = await websocket.recv()
        return response

betting=[]
lhit=[]
senddata=[]
my_result=[]
firstTime=0
whichwayx=[]
totalbetonR=[0]
totalbetonB=[0]
totalbetonL=[0]

def on_message(ws, message):
    whichway=1
    data = json.loads(message)
    if "results" in data['data']:
        whichwayx.clear()
        m=json.loads(data['data'])
        curr_result=(m['results'][0])
        print("currentResult = ", curr_result)
        print("myR = ", my_result[0])
        if(my_result[0]==curr_result):
            whichway=1
            whichwayx.append(1)
        else:
            whichway=0
            whichwayx.append(0)
        #print("whichwayx = ", whichwayx)
        betting.clear()
        lhit.clear()
        totalbetonB[0]=0
        totalbetonR[0]=0
        totalbetonL[0]=0
        my_result.clear()
        print(" BEFORE RED BET ",totalbetonR[0] )
        print(" BEFORE BLACK BET ",totalbetonB[0] )
        print(" BEFORE LUCKYHIT BET ",totalbetonL[0] )

        

    if "betInfos" in data['data']:
        data_field = data["data"]
        bet_data = json.loads(data_field)
        bet_infos = bet_data["betInfos"]
        # print(bet_infos)
        type_field = bet_infos[0]["type"]
        chipInfo_field = bet_infos[0]["chipInfo"]
        for key in chipInfo_field:
            axel=int(key)
        
        #print(chipInfo_field)
        
        if(len(betting)<=101):
            print(type_field)

            if(type_field=="R"):
                betting.append(type_field)
                totalbetonR[0]=totalbetonR[0]+axel
                print("totalbeton R = ",totalbetonR[0],"totalbeton B = ",totalbetonB[0]," and luckyhitBEt  = ",totalbetonL[0])
            elif (type_field=="B"):
                betting.append(type_field)
                totalbetonB[0]=totalbetonB[0]+axel
                print("totalbeton R = ",totalbetonR[0],"totalbeton B = ",totalbetonB[0]," and luckyhitBEt  = ",totalbetonL[0])

            else:
                lhit.append(type_field)
                totalbetonL[0]=totalbetonL[0]+axel
                print("totalbeton R = ",totalbetonR[0],"totalbeton B = ",totalbetonB[0]," and luckyhitBEt  = ",totalbetonL[0])

        if(len(betting)==101):
            if(betting.count('R')<=betting.count('B')):
                        my_result.append("R")
                        if(whichwayx[0]==1):
                            senddata=["R","R","R","R","R"]
                        elif(whichwayx[0]==0):
                            senddata=["B","B","B","B","B"]

                        #print(betting)
                        #print(betting.count('R'),"red")
                        print(lhit)
                        #print(betting.count('B'))
            else:
                        my_result.append("B")
                        if(whichwayx[0]==1):
                            senddata=["B","B","B","B","B"]
                        elif(whichwayx[0]==0
                            ):
                            senddata=["R","R","R","R","R"]
                        #print(betting)  
                        #print(betting.count('B'),"black")
                        print(lhit)
                        #print(betting.count('R'))
            json_data=json.dumps(betting)
            #print("whichwayx last =", whichwayx)
            print(" RED BET ",totalbetonR[0] )
            print(" BLACK BET ",totalbetonB[0] )
            print(lhit)
            print("now result will be ", senddata)
            asyncio.get_event_loop().run_until_complete(send_message(senddata))
    
    

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Connection closed")

ws = websocket.WebSocketApp("wss://luckyhit.cooe.in/luckyhit_ws/?token=08e59c641da96c72e854ad569f834174a9138c77",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever()

if __name__ == '__main__':
    app.run()
