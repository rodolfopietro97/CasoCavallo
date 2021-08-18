import json
import sys

from Exceptions.CasoCavalloQueuesExceptions import InvalidCasoCavalloQueueName, InvalidCasoCavalloQueueDataType, \
    InvalidRandomBytesSizeForDataTypeRandomBytes, InvalidRangeForDataType
from Utils.CasoCavalloConstants import INVALID_CHARACTERS_FOR_QUEUE_NAME, QUEUE_DATA_TYPES


class CasoCavalloConfigurationFileHandler:
    """
    Handle the fonciguration file of CasoCavallo
    """

    @staticmethod
    def import_class_using_package(name):
        """
        Import a class and package using 'reflection'

        :param name: Name of package and class

        :return: Instance of class
        """
        components = name.split('.')
        module = __import__(components[0])
        for comp in components[1:]:
            module = getattr(module, comp)
        return module

    @staticmethod
    def load_random_sources_from_configuration_file(configuration_file_path):
        """
        Load random sources contained in the configuration files

        :param configuration_file_path: Path of configuration file

        :return: Random sources on configuration file
        """

        # Random sources to use (empty default)
        random_sources = []

        try:
            # Open config.json
            config_file = json.load(open(configuration_file_path))

            # Get all random sources in configuration file
            random_sources = [
                # Class instance using 'reflection'
                # globals()[random_source['type']]()
                CasoCavalloConfigurationFileHandler.import_class_using_package(f"RandomSources."
                                                                               f"{random_source['type']}."
                                                                               f"{random_source['name']}."
                                                                               f"{random_source['name']}")
                for random_source in config_file['CasoCavalloRandomSources']
            ]

        # Missing config file
        except FileNotFoundError as file_not_foundError:
            print(f"Error on load CasoCavallo Random Number Generator. "
                  f"Missing config file \n{file_not_foundError}", file=sys.stderr)

        # Key error on json file
        except KeyError as key_error:
            print(f"Syntax error on {configuration_file_path}  \n{key_error}", file=sys.stderr)

        # Generic error
        except Exception as exception:
            print(f"Error on load CasoCavallo Random Number Generator.  \n{exception}", file=sys.stderr)

        # Return the random sources on configuration file
        return random_sources

    @staticmethod
    def load_queues_from_configuration_file(configuration_file_path):
        """
        Load random queues contained in configuration files

        :param configuration_file_path: Path of configuration file

        :return: Queues on configuration file
        """

        # Queues to use (empty default)
        queues = []

        try:
            # Open config.json
            config_file = json.load(open(configuration_file_path))

            # Get all random sources in configuration file
            queues = [
                queue
                for queue in config_file['CasoCavalloQueues']
                if CasoCavalloConfigurationFileHandler.is_valid_queue(queue)
            ]

        # Missing config file
        except FileNotFoundError as file_not_foundError:
            print(f"Error on load CasoCavallo Random Number Generator. "
                  f"Missing config file \n{file_not_foundError}", file=sys.stderr)

        # Key error on json file
        except KeyError as key_error:
            print(f"Syntax error on {configuration_file_path} Or missing a key \n{key_error}", file=sys.stderr)

        # Invalid queue name
        except InvalidCasoCavalloQueueName as invalid_queue_name:
            print(f"Error on queue names. There is an incorrect name. \n{invalid_queue_name}", file=sys.stderr)

        # Invalid queue data type
        except InvalidCasoCavalloQueueDataType as invalid_queue_data_type:
            print(f"Error on queue data types. There is an incorrect data type. \n{invalid_queue_data_type}", file=sys.stderr)

        # Invalid queue data type
        except InvalidRandomBytesSizeForDataTypeRandomBytes as invalid_random_bytes_size:
            print(f"Error on queue size. Incorrect random bytes size. \n{invalid_random_bytes_size}", file=sys.stderr)

        # Invalid queue data type
        except InvalidRangeForDataType as invalid_random_bytes_size:
            print(f"Error on queue range. Incorrect range for data type INTEGER or REAL. \n{invalid_random_bytes_size}", file=sys.stderr)

        # Generic error
        except Exception as exception:
            print(f"Error on load CasoCavallo Random Number Generator.  \n{exception}", file=sys.stderr)

        # Return the random sources on configuration file
        return queues

    @staticmethod
    def is_valid_queue(queue_to_analyze):
        """
        Validate the syntax of a queue.

        For example:
        * A BINARY queue cannot have size
        * Data types of queue must be established
        * ...

        :param queue_to_analyze:

        :return: If a queue is valid
        """

        # Name cannot contains invalid characters
        for invalid_character in INVALID_CHARACTERS_FOR_QUEUE_NAME:
            if invalid_character in queue_to_analyze['name']:
                raise InvalidCasoCavalloQueueName()

        # Check data type
        if queue_to_analyze['type'] not in QUEUE_DATA_TYPES:
            raise InvalidCasoCavalloQueueDataType()

        # Random bytes must have a size greater than 0
        if queue_to_analyze['type'] == "RANDOM_BYTES":
            if queue_to_analyze['size'] is None \
                    or \
                    not isinstance(queue_to_analyze['size'], int) \
                    or \
                    int(queue_to_analyze['size']) <= 0:
                raise InvalidRandomBytesSizeForDataTypeRandomBytes()

        # Reals must have a range
        if queue_to_analyze['type'] == "REAL":
            if len(queue_to_analyze['range']) != 2 \
                    or \
                    not (isinstance(queue_to_analyze['range'][0], float) or isinstance(queue_to_analyze['range'][0], int)) \
                    or \
                    not (isinstance(queue_to_analyze['range'][1], float) or isinstance(queue_to_analyze['range'][1], int)) \
                    or \
                    queue_to_analyze['range'][1] <= queue_to_analyze['range'][0]:
                raise InvalidRangeForDataType()

        # Integers must have a correct range
        if queue_to_analyze['type'] == "INTEGER":
            if len(queue_to_analyze['range']) != 2 \
                    or \
                    not isinstance(queue_to_analyze['range'][0], int) \
                    or \
                    not isinstance(queue_to_analyze['range'][1], int) \
                    or \
                    queue_to_analyze['range'][1] <= queue_to_analyze['range'][0]:
                raise InvalidRangeForDataType()

        # All validations are passed
        return True
