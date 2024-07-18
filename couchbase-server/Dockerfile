FROM couchbase/server:latest AS stage_base

# Install unzip if it's not available
RUN apt-get update && apt-get install -y unzip

# Copy the json.zip files into the Docker image
COPY *.json.zip ./

# Unzip all json files in the current directory
RUN for file in *.json.zip; do unzip "$file"; done
RUN mkdir -p /opt/couchbase/init/
RUN mv ./*.json /opt/couchbase/init/
RUN rm *.zip

COPY init-cbserver.sh /opt/couchbase/init/
#update permissions to run the script
RUN chmod +x /opt/couchbase/init/init-cbserver.sh