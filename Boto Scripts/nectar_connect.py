import boto
from boto.ec2.regioninfo import RegionInfo

region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

ec2_conn = boto.connect_ec2(
	aws_access_key_id='6a418d0ccdc54f3297c8fba9ea74e0de',
	aws_secret_access_key='ed523da739c644e99a926f411d8d17f9',
	is_secure=True,
	region=region,
	port=8773,
	path='/services/Cloud',
	validate_certs=False) 