# Docker Setup

**Warning**:  The passwords for the Couchbase Server Administration user and the Sync use are set in the docker-compose.yml file for both the Couchbase Server definition and the Sync Gateway Server.  The Sync Gateway init-syncgateway.sh file also has hardcoded username and password.  You should probably change these passwords if you are a security conscious person.  I bare no blame if someone hacks your system because you didn't change the passwords.  

To setup the latest version of Couchbase Server and Sync Gateway with all the sample data for the learning set run the following command:

```bash
docker-compose -p couchbase-environment up -d
```

Note you can name the project/environment name anything you want after the -p statement.  In the example I named the environment `couchbase-environment`.  

## Testing Data

To test that the data has been loaded correctly in Sync Gateway:

- Wait for the containers to start
- The Sync Gateway container should have a message in the logs `Creating sales database for syncing warehouse collection`.  Wait for 15 seconds after this message.
- Open a terminal to the Sync Gateway container and run the following commands listed below which are calls to the Admin REST API

**Note** The --user is the username and password from the config file.  If you changed these in the docker compose file, you will have to change the example commands before running them.


### Database Config:
```bash
curl -X GET "http://localhost:4985/audit/_config?include_javascript=true" -H "accept: application/json" --user "sync:P@33w0rdS7nc" 
curl -X GET "http://localhost:4985/sales/_config?include_javascript=true" -H "accept: application/json" --user "sync:P@33w0rdS7nc" 
```

### Roles:
```bash
curl -X GET "http://localhost:4985/audit/_role/" -H "accept: application/json" --user "sync:P@33w0rdS7nc" 
```

### Users:
```bash
curl -X GET "http://localhost:4985/audit/_user/?name_only=false" -H "accept: application/json" --user "sync:P@33w0rdS7nc" 
curl -X GET "http://localhost:4985/sales/_user/?name_only=false" -H "accept: application/json" --user "sync:P@33w0rdS7nc" 
```

### Check User Details:
```bash
curl -X GET "http://localhost:4985/audit/_user/demo@example.com" -H "accept: application/json" --user "sync:P@33w0rdS7nc" 
curl -X GET "http://localhost:4985/audit/_user/demo1@example.com" -H "accept: application/json" --user "sync:P@33w0rdS7nc" 
```

### Documents:
```bash
curl -X GET "http://localhost:4985/audit.audit.inventory/_all_docs?limit=100" -H "accept: application/json" --user "sync:P@33w0rdS7nc" 
curl -X GET "http://localhost:4985/audit.audit.projects/_all_docs?limit=100" -H "accept: application/json" --user "sync:P@33w0rdS7nc" 
curl -X GET "http://localhost:4985/sales.sales.warehouse/_all_docs?limit=100" -H "accept: application/json" --user "sync:P@33w0rdS7nc" 
curl -X GET "http://localhost:4985/audit.audit.userProfiles/_all_docs?limit=100" -H "accept: application/json" --user "sync:P@33w0rdS7nc" 
```

## YouTube Video Tutorial

A YouTube video is available for those looking for a deep dive into how everything works at [https://www.youtube.com/watch?v=X0hL1Z32ck0](https://www.youtube.com/watch?v=X0hL1Z32ck0)