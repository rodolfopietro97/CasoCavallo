# Nodejs image
FROM node

# Create working directory
WORKDIR /app/casocavallo_p2p_layer

# Update node
RUN npm install -g npm@latest

# Install Global dependendencies
RUN npm install -g typescript && npm install -g grpc-tools

# Install local dependencies
COPY package*.json /app/casocavallo_p2p_layer/
RUN npm install

# Create node_modules volume to avoid problems on run npm install
VOLUME [ "/app/casocavallo_p2p_layer", "/app/casocavallo_p2p_layer/node_modules" ]

# Uncomment if you want to use docker run/build directly.
# CMD is already in docker-compose
# CMD [ "npm", "run", "serve" ]