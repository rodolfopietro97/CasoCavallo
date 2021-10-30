from time import sleep

from Utils.CasoCavalloConstants import MESSAGE_ENCODING, SERVER_SOLVING_TIME
from Utils.CummareApi.CummreClient import subscribe, publish

import json

import rsa

import base64


random_requests = {}
"""
Random requests to solve
"""


def push_random_requests(random_request):
    """
    Solve random requests

    :param random_request: Random request to solve
    """

    # Remove timestamp form request
    random_request_without_timestamp = json.loads(random_request.strip())
    del random_request_without_timestamp['timestamp']

    random_request_without_timestamp_as_string = json.dumps(random_request_without_timestamp)

    # Add to requests if not exists
    if random_request_without_timestamp_as_string not in random_requests:
        # Set as not solved
        random_requests[random_request_without_timestamp_as_string] = False


def server_worker(redis_client, redis_lists, cummare_server):
    """
    Real time server.
    Every seconds it handle random requests and push random responses

    :param redis_client: Redis client ot use
    :param redis_lists: Redis lists names that we want show
    :param cummare_server: Address of Cummare Server
    """

    # Predefined topics for requests and responses
    requests_topic = "random_requests"
    responses_topic = "random_responses"

    # For each redis list init currents random numbers
    currents_randoms = {}

    # Run forever
    while True:

        # Update currents randoms
        for queue in redis_lists:
            currents_randoms[queue] = redis_client.get(f'current_{queue}').decode()

        # Create command and execute it
        subscribe(cummare_server=cummare_server,
                                    topic=requests_topic,
                                    process_function=push_random_requests)

        # Solve all requests
        for random_request in random_requests:

            # Object version of request
            random_request_object = json.loads(random_request)

            # Not solved
            if not random_requests[random_request]:

                # If queue is valid
                if random_request_object['queue'] in redis_lists:

                    # Get public key
                    encryption_public_key = rsa.PublicKey.load_pkcs1(random_request_object['public_key'].encode(MESSAGE_ENCODING), format='PEM')

                    # Encode message
                    message_to_send_in_bytes = str(
                        currents_randoms[
                            random_request_object['queue']
                        ]
                    ).encode(MESSAGE_ENCODING)

                    # Encrypt message
                    encrypt_message = rsa.encrypt(message_to_send_in_bytes, encryption_public_key)
                    encrypt_message_string = encrypt_message.decode(MESSAGE_ENCODING)

                    # Init data on random response
                    random_response_solved = random_request_object
                    random_response_solved['data'] = base64.b64encode(encrypt_message_string.encode(MESSAGE_ENCODING)).decode()

                    # Set request as solved
                    random_requests[random_request] = True

                    # Send response
                    publish(cummare_server=cummare_server, topic=responses_topic, message=str(json.dumps(random_response_solved)))

        sleep(SERVER_SOLVING_TIME)
