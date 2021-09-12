# Nodejs image
FROM node

# Create working directory
WORKDIR /app/casocavallo/p2p_layer

# Install Global dependendencies
RUN npm install -g typescript

# Install local dependencies
COPY package*.json /app/casocavallo/p2p_layer/
RUN npm install

# Create node_modules volume to avoid problems on run npm install
VOLUME [ "/app/casocavallo/p2p_layer", "/app/casocavallo/p2p_layer/node_modules" ]

# Uncomment if you want to use docker run/build directly.
# CMD is already in docker-compose
# CMD [ "npm", "run", "serve" ]