from Utils.ConfigurationFiles.CasoCavalloConfigurationFileHandler import CasoCavalloConfigurationFileHandler
from Utils.CasoCavalloConstants import CONFIGURATION_FILE_PATH
from Workers.PerformanceTester import performance_tester_worker

if __name__ == '__main__':
    """
    Main method
    """

    # ***** 1) Fetch random sources from configuration file *****
    random_sources = CasoCavalloConfigurationFileHandler \
        .load_random_sources_from_configuration_file(CONFIGURATION_FILE_PATH)

    # Do initial performances tests
    performance_tester_worker(random_sources=random_sources)
