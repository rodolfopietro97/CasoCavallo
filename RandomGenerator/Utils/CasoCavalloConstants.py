HEX_ALPHABET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
"""
Alphabet of hexadecimal numbers
"""


REDIS_SERVER = {
    'host': '1.0.0.10',
    'port': 6379,
    'database': 0
}
"""
Redis server informations.

This configuration is the default uses on docker
"""


CONFIGURATION_FILE_PATH = "./Config.json"
"""
Path of configuration file.

Configuration file contains random sources to use and a lot of stuffs
"""


INITIAL_PERFORMANCES_TEST = False
"""
If do or not initial performance test.
Initial performance test told to us:

"How many pair of random bytes of 32 bytes i can generate in 1 seconds.
And every time i make xor operation between them.
All for each random source i use"

"""


RANDOM_GENERATION_TIME = 1
"""
Second after that we must generate a new random
"""


RANDOM_REMOVAL_TIME = 1.5
"""
Second after that we must remove a random from list
"""


RANDOM_THRESHOLD = 100
"""
Indicate the size of the internal random queue.

It says "How many random numbers i must have in my Redis queue?"
"""


USE_VIEWER = True
"""
If use or not real time viewer
"""


VIEWER_MAXIMUM_ROWS = 10
"""
Number of rows to show using viewer
"""


VIEWER_PRINT_TIME = 1
"""
Print redis lists every VIEWER_PRINT_TIME seconds
"""


INVALID_CHARACTERS_FOR_QUEUE_NAME = [" "]
"""
Invalid characters for a queue name
"""


QUEUE_DATA_TYPES = [
    "BINARY",
    "RANDOM_BYTES",
    "REAL",
    "INTEGER"
]
"""
Data types for random queues
"""