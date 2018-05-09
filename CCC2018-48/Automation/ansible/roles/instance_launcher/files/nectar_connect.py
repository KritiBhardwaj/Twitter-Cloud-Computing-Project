#Team 48
#Muhammad Umair, ID: 863579
#Kriti Bhardwaj, ID: 880873
#Haaris Nazir Ahmed, ID: 869969
#Sergey Germogentov, ID: 893900

import boto
from boto.ec2.regioninfo import RegionInfo

region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

ec2_conn = boto.connect_ec2(
	aws_access_key_id='1a008c21141944e6b00c87e0bec03479',
	aws_secret_access_key='212942d5fe9448f28e813552f726aaee',
	is_secure=True,
	region=region,
	port=8773,
	path='/services/Cloud',
	validate_certs=False) 