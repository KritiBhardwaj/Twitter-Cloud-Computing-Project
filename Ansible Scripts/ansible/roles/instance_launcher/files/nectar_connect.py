import boto
from boto.ec2.regioninfo import RegionInfo

region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

ec2_conn = boto.connect_ec2(
	aws_access_key_id='575d0e928b7a4617b10cbecd66afe812',
	aws_secret_access_key='f49cddca4108493eac99482b76a854bc',
	is_secure=True,
	region=region,
	port=8773,
	path='/services/Cloud',
	validate_certs=False) 