#!/usr/bin/python3
import unittest

from lib.ConnectionUtilities import create_connection_from_config
from lib.CredentialUtilities import create_user
from lib.SecretUtilities import create_keypair, update_keypair
from lib.DatabaseUtilities import \
    create_db_connection,\
    get_network_name,\
    add_instance_to_user,\
    remove_instance_from_user,\
    create_image_document,\
    get_keypair

conn = create_connection_from_config()
client = create_db_connection()
db = client["t2ee"]

class test_keypair(unittest.TestCase):
    def test_create_keypair_openstack(self):
        create_keypair("test_user1", 
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDIQsqACwJNdccD87Li27fvnBuIjdZNewxZwKLxnT8p/N8S/dHNBgAbyQhcI753ErtesMQhgaRViFJIXMFsG1zCbDbE4b6pKKiLGlF7+OzrtX7vcsDeiblgakT73Rlcfq1SmZhow9whZgKefTyjxBDrjwj3lSuCCD3z9w3sIEKXszb5FtmcfC814Pqccyvde9ZX4KmVpo3ygGiUA6xQ/+Ky+dEm+nm1VoEseSD6SqKWC6oNHmIwI6LKfkb8pYxdwj6GqF3if4J0Jl5njfk9svUo60v8B3mu+FT1K8JNHzPhTINPS+Jp+EwmOSSqipKZ0SfsCfeOYuUM0HLFdETSdq6G3zt7aUSTAyOGTJXrGz8abdoB1gwqfgbat8V5SKflcsR6NdpiheMVqXaSNxeivpCxBslytQPIESpvvmjEW1S+2bnWmN9GpKHDJEb5ENrBRvHez38ulFPMsS9IgucB4vt3KfhSC5MVGjMqu0x13gg2T8gR+9Fg1HdSdyY7BM2x6atl96peS5SIXZrj3x6m/7RSzvR88M3cOyuCYQzQXA1gPtxB7DidHKbQwyopKJG6r6hOsKJgbDzwdrTHvXKK8Xzbj56i9P1avWwuo+tpkIX52ZFhIAYAkoY/gePOpe94m9ddsYqqY9UUBJ0JI81kcAVTLDHbSYNXaNPNDvLzM7R4vw== root@t2ee")

    def test_update_keypair(self):
        update_keypair("test_user1",
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDS7ccrAx5T3LFHSElcyjaTavfdG+8JBzk0RscUHbkQGKTTdoaQGlTduCQDJLt86KpkrBOK2fklcU1O0Q02Y8Y1Zdrns6zwNb8czgKi0qAyUZ2GwAtFNTeLrpRk4g4J6+gD8HSPDxXqVLrOXF+LEN7gqzEQcpcpl1c2qzoS5VspbVWwcak7Jc6sGppjrqa1vUo/zdz90HQQ6SoiEjTDsQeB7DDvOeefSFJMLL9siBH884OIVyvTUQWFkr/vUwGL7g9oGvHUymLcjKY+SnjCoIEo2gM4pLhwhzNtwadv8plKwdyGjG+Fsq3Dzm1RmA9gOHRVWPmcKDQQM2vPbzQs/LqL Generated-by-Nova")

    def test_get_keypair(self):
        key = get_keypair("test_user1")
        self.assertEqual("test_user1_key", key)
        
if __name__ == '__main__':
    unittest.main()