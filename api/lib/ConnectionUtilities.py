import openstack
import yaml


# Class: options
# Date: 2019/12/30
# Purpose: Creation options for creating connection from openstack.yaml config file

class options(object):
    def __init__(self, file = "config/openstack.yaml", debug=False):
        with open(file, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        self.auth_url = data_loaded['auth']['auth_url']
        self.username = data_loaded['auth']['username']
        self.password = data_loaded['auth']['password']
        self.project_name = data_loaded['auth']['project_name']
        self.user_domain_name = data_loaded['auth']['user_domain_name']
        self.project_domain_name = data_loaded['auth']['project_domain_name']
        self.identity_api_version = data_loaded['auth']['identity_api_version']
        self.image_api_version = data_loaded['auth']['image_api_version']
        
        self.region_name = data_loaded['region_name']


# Function: create_connection_from_config
# Date: 2019/12/30
# Purpose: Create OpenStack connection
# Parameters:
#     None
# Return value:
#     openstack.connection.Connection object

def create_connection_from_config(file="config/openstack.yaml"):
    opts = options(file)
    return openstack.connection.Connection(
        auth_url = opts.auth_url,
        username = opts.username,
        password = opts.password,
        project_name = opts.project_name,
        region_name = opts.region_name,
        project_domain_name = opts.project_domain_name,
        user_domain_name = opts.user_domain_name,
        identity_api_version = opts.identity_api_version,
        image_api_version = opts.image_api_version
    )