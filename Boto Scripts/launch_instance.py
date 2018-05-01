import sys
import time
from nectar_connect import ec2_conn

# specify...
# the number of instances to launch
num_of_instances = sys.argv[1]
# the type of the instance
instance_type = "m2.tiny"
# system image to launch (retrieved from 'list_images.py')
system_image = 'ami-190a1773'

# Establishes connection with NeCTAR
print("Connecting to NeCTAR and launching instances...")
reservation = ec2_conn.run_instances('ami-190a1773',
	min_count=num_of_instances,
	max_count=num_of_instances,
	key_name='sergeykey',
	placement='melbourne',
	instance_type=instance_type,
	security_groups=['ssh'])

instances = reservation.instances

# Creates new instances
for instance in instances:
	print("New instance {} has been created.".format(instance.id))

# The IP addresses of newly created instances 
# will be recorded in the Ansible "hosts" file
file = open("hosts","w")
file.write("[harvesters]\n")

# Waits until instances are in the running state
print("Waiting till the instances are ready...")
for instance in instances:
	while (instance.update() != "running"):
		time.sleep(1)
	file.write("{}\n".format(instance.private_ip_address))
	print("The instance {} is ready.".format(instance.id))

file.close()
	