sudo -s
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:couchdb/stable
sudo apt-get update
sudo apt-get install couchdb -y
chown -R couchdb:couchdb /usr/bin/couchdb /etc/couchdb /usr/share/couchdb
chmod -R 0770 /usr/bin/couchdb /etc/couchdb /usr/share/couchdb
systemctl restart couchdb
curl localhost:5984