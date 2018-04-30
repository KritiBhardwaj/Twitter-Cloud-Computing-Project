import sys
from nectar_connect import ec2_conn

# specify...
# the number of instances to launch
num_of_instances = sys.argv[1]
# the type of the instance
instance_type = "m2.tiny"
# system image to launch (retrieved from 'list_images.py')
system_image = 'ami-190a1773'

reservation = ec2_conn.run_instances('ami-190a1773',
	min_count=num_of_instances,
	max_count=num_of_instances,
	key_name='sergeykey',
	placement='melbourne',
	instance_type=instance_type,
	security_groups=['ssh'])

instances = reservation.instances

for instance in instances:
	print("New instance {} has been created.".format(instance.id))