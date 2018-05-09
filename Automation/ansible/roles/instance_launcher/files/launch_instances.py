import sys
import time
import random
import json
from nectar_connect import ec2_conn

#Divide tasks for each harvester.
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



# specify...
# the number of instances to launch
num_of_instances = sys.argv[1]
# the type of the instance
instance_type = "m2.tiny"
# system image to launch (retrieved from 'list_images.py')
system_image = 'ami-190a1773'

# Establishes connection with NeCTAR
print("Connecting to NeCTAR and launching instances...")
reservation = ec2_conn.run_instances(
	system_image,
	min_count=num_of_instances,
	max_count=num_of_instances,
	key_name='cloudcc',
	placement='melbourne',
	instance_type=instance_type,
	security_groups=['harvesters'])

instances = reservation.instances

# Creates new instances
for instance in instances:
	print("New instance {} has been created.".format(instance.id))

# The IP addresses of newly created instances 
# will be recorded in the Ansible "hosts" file
file = open("hosts","w")
file.write("[harvesters]\n")
#Do coordinates calculations here!
numberOfHarvesters=len(instances)
#melbourneCoords='{"longMax":100,"latMin":0,"longMin":0,"latMax":100}'
melbourneCoords='{"longMin":144.5937,"latMin":-38.4339,"longMax":145.5125,"latMax":-37.5113}'
box=json.loads(melbourneCoords)
j=divideGridEvolved(box,numberOfHarvesters)
count=0
#for x in j:
#    count+=1
#    #print(x)
#    j=json.loads(x)
#    print(j)
#    #print("Rect-"+str(count)+": longMax:"+str(j["longMax"])+" | latMin:"+str(j["latMin"])+" | longMin:"+str(j["longMin"])+" | latMax:"+str(j["latMax"]))
#    print(j['latMin'],",",j['longMin'],j['latMax'],",",j['longMax'])



# Waits until instances are in the running state
print("Waiting till the instances are ready...")
instanceCount=0
print(j)
for instance in instances:
	while (instance.update() != "running"):
		time.sleep(1)
	#Assign coordinates configurations here.
	k=json.loads(j[instanceCount])
	instanceCount+=1
	file.write("{}\n"
		.format(instance.private_ip_address + 
		" harvester_id=" + format(instance.id)+
		" longMin="+str(k['longMin'])+ 
		" latMin="+str(k['latMin'])+ 
		" longMax="+str(k['longMax'])+ 
		" latMax="+str(k['latMax'])+ 
		" instanceCount="+str(instanceCount)+ 
		" ansible_python_interpreter=/usr/bin/python3"))
		
	print("The instance {} is ready.".format(instance.id))


file.close()

# Waits to avoid "Connection refused" errors in Ansible
print("Waiting to finalise instances' network configuration...")
time.sleep(60)