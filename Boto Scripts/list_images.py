from nectar_connect import ec2_conn

images = ec2_conn.get_all_images()

for img in images:
	print("Image ID: {}, image name: {}".format(img.id, img.name))

# Image ID: ami-190a1773, image name: NeCTAR Ubuntu 16.04 LTS (Xenial) amd64
# Image ID: ami-8aac485a, image name: NeCTAR Ubuntu 14.04 (Trusty) amd64
