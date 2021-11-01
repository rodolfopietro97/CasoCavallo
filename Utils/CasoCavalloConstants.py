HEX_ALPHABET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
"""
Alphabet of hexadecimal numbers
"""


CONFIGURATION_FILE_PATH = "../Configurations/CasoCavalloConfig.json"
"""
Path of configuration file.

Configuration file contains random sources to use and a lot of stuffs
"""


RANDOM_GENERATION_TIME = 0.03
"""
Second after that we must generate a new random
"""


RANDOM_REMOVAL_TIME = 0.07
"""
Second after that we must remove a random from list
"""


RANDOM_THRESHOLD = 30
"""
Indicate the size of the internal random queue.

It says "How many random numbers i must have in my Redis queue?"
"""


VIEWER_MAXIMUM_ROWS = 5
"""
Number of rows to show using viewer
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


MERGER_BUFFER_SIZE = 10
"""
Size of buffer uses for merge random numbers of a queues in a single random number.

For example, we have the queue 'my_32_bytes_queue'. The merger process make a random
sample from this queue of MERGER_BUFFER_SIZE size.
And after concatenates all numbers (with different strategies)
"""


MERGER_MERGE_TIME = 0.05
"""
After how many MERGER_MERGE_TIME merge process must do merge of numbers
in each queue
"""
