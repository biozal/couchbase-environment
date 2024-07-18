#!/bin/bash
# used to start sync - can't get around this as docker compose only allows you to start one command - so we have to start sync gateway like the standard sync gateway Dockerfile would 
# https://github.com/couchbase/docker/blob/master/enterprise/sync-gateway/3.0.3/Dockerfile#L27

# track if setup is complete so we don't try to setup again
FILE="$HOME/logs/setupComplete.txt"

if ! [ -f "$FILE" ]; then
	sleep 25s
	# create file so we know that the cluster is setup and don't run the setup again
	/entrypoint.sh /etc/sync_gateway/sync_gateway.json & 

	sleep 30s
    # https://docs.couchbase.com/sync-gateway/current/configuration-schema-database.html

	#create databases for each scope - a database is limited to 1 scope and 1000 collections
	# https://docs.couchbase.com/sync-gateway/current/configuration-schema-database.html
	# https://docs.couchbase.com/sync-gateway/current/scopes-and-collections-config.html
	echo -e "Creating audit database for syncing projects and inventory collections\n"
AUTHUSER="$COUCHBASE_RBAC_USERNAME:$COUCHBASE_RBAC_PASSWORD"

/bin/curl --location --request PUT 'http://localhost:4985/audit/' \
--user "$AUTHUSER" \
--header 'Content-Type: application/json' \
--data-raw '{
  "bucket": "inventoryDemo",
  "num_index_replicas": 0,
  "scopes": {
  	"audit": {
  		"collections": {
  			"projects":{
  			  "sync": "function(doc, oldDoc, meta) { try { console.log(\"********Processing Project Docs\"); validateNotEmpty(\"teams\", doc.teams); var teams = getTeams(); teams.forEach(function (team) { requireRole(team); if (!isDelete()) {  var channelId = \"channel.\" + team; console.log(\"********Setting Project Channel to \" + channelId);  channel(channelId); access(\"role:\" + team, \"channel.\" + team); } }); } catch (e) { console.log(\"***************Error Processing Project Docs: \" + e); } function getTeams() {  return isDelete() ? oldDoc.teams : doc.teams; } function isDelete() { return doc._deleted == true; } function validateNotEmpty(key, value) { if (!value) { throw {forbidden: key + \" is not provided.\"}; } } }",
         	"import_filter": "function(doc) { if (doc.isActive){ return true; } return false; }"
       	},
        "inventory":{
          "sync": "function(doc, oldDoc, meta) { try { console.log(\"********Processing Inventory Docs\"); validateNotEmpty(\"teams\", doc.teams); var teams = getTeams(); teams.forEach(function (team) { requireRole(team); if (!isDelete()) { var channelId = \"channel.\" + team; console.log(\"********Setting Inventory Channel to \" + channelId); channel(channelId); access(\"role:\" + team, \"channel.\" + team); } }); } catch (e) { console.log(\"***************Error Processing Inventory Docs:\" + e); } function getTeams() { return isDelete() ? oldDoc.teams : doc.teams; } function isDelete() { return doc._deleted == true; } function validateNotEmpty(key, value) { if (!value) { throw {forbidden: key + \" is not provided.\"}; } } }",
         	"import_filter": "function(doc) { if (doc.isActive){ return true; } return false; }"
        },
        "userProfiles":{
  				"sync": "function(doc, oldDoc, meta) { console.log(\"********Processing User Profile Doc. Is oldDoc == null? \" + (oldDoc == null)); validateNotEmpty(\"email\", doc.email); var expectedDocId = \"user\" + \"::\" + doc.email; if (expectedDocId != doc._id) { throw({forbidden: \"UserProfile doc Id must be of form user::email\"}); } var username = getEmail(); var channelId = \"channel.\"+ username; try { channel(\"!\"); requireAdmin(); if (!isDelete()) { channel(channelId); access(username, channelId); } } catch (error) { console.log(\"UserProfile - This is not a doc import \" + error); if (!isDelete()) { if (isCreate()) { channel(channelId); access(username, channelId); } else { validateReadOnly(\"email\", doc.email, oldDoc.email); requireUser(oldDoc.email); } } } function getEmail() { return (isDelete() ? oldDoc.email : doc.email); } function isCreate() { return ((oldDoc == false) || (oldDoc == null || oldDoc._deleted) && !isDelete()); } function isDelete() { return (doc._deleted == true); } function validateNotEmpty(key, value) { if (!value) { throw({forbidden: key + \" is not provided.\"}); } } function validateReadOnly(name, value, oldValue) { if (value != oldValue) { throw({forbidden: name + \" is read-only.\"}); } } }",
  				"import_filter": "function(doc) { if (doc.isActive === true){ return true; } return false; }"
  	    }
      }
    }
 	}
}'

echo -e "Creating roles for audit\n"

# Define an array of role and usernames
declare -a users=("demo@example.com" "demo1@example.com" "demo2@example.com" "demo3@example.com" "demo4@example.com" "demo5@example.com" "demo6@example.com" "demo7@example.com" "demo8@example.com" "demo9@example.com" "demo10@example.com" "demo11@example.com" "demo12@example.com" "demo13@example.com" "demo14@example.com" "demo15@example.com" "demo16@example.com" "demo17@example.com" "demo18@example.com" "demo19@example.com" "demo20@example.com" "demo21@example.com" "demo22@example.com" "demo23@example.com" "demo24@example.com")

declare -a roles=("AL" "AK" "AZ" "AR" "AS" "CA" "CO" "CT" "DE" "DC" "FL" "GA" "GU" "HI" "ID" "IL" "IN" "IA" "KS" "KY" "LA" "ME" "MD" "MA" "MI" "MN" "MS" "MO" "MT" "NE" "NV" "NH" "NJ" "NM" "NY" "NC" "ND" "MP" "OH" "OK" "OR" "PA" "PR" "RI" "SC" "SD" "TN" "TX" "TT" "UT" "VT" "VI" "VA" "WA" "WV" "WI" "WY")
# Iterate the string array using for loop to add roles
for role in "${roles[@]}"
do
  /bin/curl --location --request POST 'http://localhost:4985/audit/_role/' \
  --user "$AUTHUSER" \
  --header 'Content-Type: application/json' \
  --data-raw $'{"name":"'"$role"'","collection_access":{"audit":{"projects":{"admin_channels":["'"$role"'"]},"inventory":{"admin_channels":["'"$role"'"]}}}}'
done

# add users for audit database
# start with admin user

echo -e "Creating users for audit\n"
/bin/curl --location --request POST 'http://localhost:4985/audit/_user/' \
--user "$AUTHUSER" \
--header 'Content-Type: application/json' \
--data-raw $'{ "password": "P@ssw0rd12", "admin_roles": ["AL", "AK", "AZ", "AR", "CA", "CO", "CA", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"], "name": "demo@example.com", "email": "demo@example.com" }'

#define a counter for calculating the admin role
counter=0
for user in "${users[@]}"
do
  if [ "$user" == "demo@example.com" ]; then
    counter=$((counter+1))
    continue
  fi
  # calculate the admin role, we need two users to test each admin role
  case $counter in
    1|2)
      admin_roles='["AZ", "CA", "HI", "NV"]'
      ;;
    3|4)
      admin_roles='["AR", "LA", "NM", "OK", "TX"]'
      ;;
    5|6)
      admin_roles='["AL", "FL", "MS"]'
      ;;
    7|8)
      admin_roles='["CT", "MA", "ME", "NH", "NJ", "NY", "RI", "VT"]'
      ;;
    9|10)
      admin_roles='["IA", "IL", "IN", "MN", "WI"]'
      ;;
    11|12)
      admin_roles='["GA", "NC", "SC"]'
      ;;
    13|14)
      admin_roles='["AK", "ID", "OR", "WA"]'
      ;;
    15|16)
      admin_roles='["CO", "MT", "UT", "WY"]'
      ;;
    17|18)
      admin_roles='["DC", "DE", "MD", "PA", "VA", "WV"]'
      ;;
    19|20)
      admin_roles='["MI", "OH"]'
      ;;
    21|22)
      admin_roles='["KS", "ND", "NE", "SD"]'
      ;;
    23|24)
      admin_roles='["KY", "MO", "TN"]'
    ;;
    *)
    ;;
  esac

  echo -e "Creating user $user for audit database\n"
  # add the actual user
  /bin/curl --location --request POST 'http://localhost:4985/audit/_user/' \
  --user "$AUTHUSER" \
  --header 'Content-Type: application/json' \
  --data-raw "{ \"password\": \"P@ssw0rd12\", \"admin_channels\": [\"channel.$user\"], \"admin_roles\": $admin_roles, \"name\": \"$user\", \"email\": \"$user\"}"
  counter=$((counter+1))
done

	echo -e "Creating sales database for syncing warehouse collection\n"
	/bin/curl --location --request PUT 'http://localhost:4985/sales/' \
  --user "$AUTHUSER" \
	--header 'Content-Type: application/json' \
	--data-raw '{
                "bucket": "inventoryDemo",
                "num_index_replicas": 0,
                "scopes": {
                  "sales": {
                    "collections": {
                      "warehouse":{
                        "sync": "function(doc, oldDoc, meta) { channel(\"!\"); if (oldDoc || doc._deleted) { throw({forbidden: \"Modifications are not allowed\"}); } }",
                        "import_filter": "function(doc) { if (doc.isActive === true){ return true; } return false; }"
                      }
                    }
                  }
                }
              }'

# Iterate the string array using for loop to add roles
for user in "${users[@]}"
do
  #create users - sales database
/bin/curl --location --request POST 'http://localhost:4985/sales/_user/' \
--user "$AUTHUSER" \
--header 'Content-Type: application/json' \
--data-raw "{\"password\": \"P@ssw0rd12\", \"name\": \"$user\", \"email\": \"$user\"}"
done

touch "$FILE"

else 
	sleep 10s 
	/entrypoint.sh /etc/sync_gateway/config.json & 
fi

# docker compose will stop the container from running unless we do this
# known issue and workaround
tail -f /dev/null