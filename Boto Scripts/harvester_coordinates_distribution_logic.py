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
    diffLats=H-B
    incrementalDifference=(diffLats/n)
    count=0
    prevLat=B
    for x in range((numberOfPoints*2)+1):
        if(x==2 and x%2==0):
            count+=1
            latitude='latMax'
            value=prevLat+incrementalDifference
            prevLat=value
            result='{"longMax": '+str(A)+' , "latMin": '+str(B)+' , "longMin": '+str(G)+' , "'+latitude+'": '+str(value)+'}'
            listCoords.append(result)
        elif(x!=0 and x%2==0):
            count+=1
            latitude='latMax'
            value=prevLat+incrementalDifference
            result='{"longMax": '+str(A)+' , "latMin": '+str(prevLat)+' , "longMin": '+str(G)+' , "'+latitude+'": '+str(value)+'}'
            prevLat=value
            listCoords.append(result)
    return  listCoords



#melbourneCoords='{"longMax":100,"latMin":0,"longMin":0,"latMax":100}'
melbourneCoords='{"longMax":144.5937,"latMin":-38.4339,"longMin":145.5125,"latMax":-37.5113}'
box=json.loads(melbourneCoords)
j=divideGridEvolved(box,numberOfHarvesters)
count=0
for x in j:
    count+=1
    j=json.loads(x)
    #print(j)
    print("Rect-"+str(count)+": longMax:"+str(j["longMax"])+" | latMin:"+str(j["latMin"])+" | longMin:"+str(j["longMin"])+" | latMax:"+str(j["latMax"]))
