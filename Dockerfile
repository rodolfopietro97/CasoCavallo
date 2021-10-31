# Pythoh image
FROM python

# Create working directory
WORKDIR /app/casocavallo/random_generator

# Copy all files in working directory
COPY . /app/casocavallo/random_generator

# Install requirements
RUN pip install -r requirements.txt

# Create volumes for development purposes. 
# 1) If we modify files is not needed to run new time docker-compose build
# 2) Volume for configuration files
VOLUME [ "/app/casocavallo/random_generator", "/app/casocavallo/Configurations" ]

# Uncomment if you want to use docker run/build directly.
# CMD is already in docker-compose
# CMD [ "python", "Generator.py" ]