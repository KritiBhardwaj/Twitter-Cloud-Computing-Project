#Team 48
#Muhammad Umair, ID: 863579
#Kriti Bhardwaj, ID: 880873
#Haaris Nazir Ahmed, ID: 869969
#Sergey Germogentov, ID: 

import json

numberOfHarvesters=4

def divideGridEvolved(box,n):
    #Construct the box first!
    A=box['longMax']
    B=box['latMin']
    C=box['longMax']
    D=box['latMax']
    E=box['longMin']
    F=box['latMin']
    G=box['longMin']
    H=box['latMax']
    listCoords=[]
    numberOfPoints=n
    diffLats=H-F
    incrementalDifference=(diffLats/n)
    count=0
    prevLat=F
    for x in range((numberOfPoints*2)+1):
        if(x==2 and x%2==0):
            count+=1
            latitude='latMax'
            value=prevLat+incrementalDifference
            prevLat=value
            result='{"longMin": '+str(E)+' , "latMin": '+str(B)+' , "longMax": '+str(A)+' , "'+latitude+'": '+str(value)+'}'
            listCoords.append(result)
        elif(x!=0 and x%2==0):
            count+=1
            latitude='latMax'
            value=prevLat+incrementalDifference
            result='{"longMin": '+str(E)+' , "latMin": '+str(prevLat)+' , "longMax": '+str(A)+' , "'+latitude+'": '+str(value)+'}'
            prevLat=value
            listCoords.append(result)
    return  listCoords



#melbourneCoords='{"longMax":100,"latMin":0,"longMin":0,"latMax":100}'
melbourneCoords='{"longMin":144.5937,"latMin":-38.4339,"longMax":145.5125,"latMax":-37.5113}'
box=json.loads(melbourneCoords)
j=divideGridEvolved(box,numberOfHarvesters)
count=0
#{"longMin": 144.5937 , "latMin": -37.74195 , "longMax": 145.5125 , "latMax": -37.511300000000006}
k=json.loads(j[0])
for x in j:
    count+=1
    #print(x)
    j=json.loads(x)
    #print(j)
    #print("Rect-"+str(count)+": longMax:"+str(j["longMax"])+" | latMin:"+str(j["latMin"])+" | longMin:"+str(j["longMin"])+" | latMax:"+str(j["latMax"]))
    print(j['latMin'],",",j['longMin'])
    print(j['latMax'],",",j['longMax'])
    print("\n")
