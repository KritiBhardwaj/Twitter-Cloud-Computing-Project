#For getting ansible up on a new server, run the commands below (Tested at Ubuntu Xenial)
sudo pip3 install ansible
sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible -y
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
sudo pip3 install cryptography --upgrade

#Replace files of the ansible folder with the one provided here "ansible". Make sure Ubuntu user owns the folder.
#Run the command below.
ansible-playbook -i ./hosts ./twitharvester.yaml --private-key=~/.ssh/cloudcc.pem -u ubuntu --extra-vars "numinstances=2"
