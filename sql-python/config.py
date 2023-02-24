import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://icj-cosmos-db.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'vjF9Q0FVpXA5pxAOJRgfDrJdGRdZL2MRuE45JQkUdnB7O1sIU68GP2IofbdZ6snPMasEBre6GhNfACDbdY6T8A=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'ToDoList'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Items'),
}