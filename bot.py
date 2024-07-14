"""
This script automates the process of posting updates to Twitter based on the analysis of athletics records data.

Workflow:
1. Authenticate with the Twitter API using credentials.
2. Load and analyze athletics records data to identify noteworthy changes or updates.
3. Generate tweet messages based on the analysis.
4. Post the generated messages to Twitter.
5. Synchronize data folders by moving processed data for archival and preparing for the next analysis cycle.
6. Log all operations and their outcomes for monitoring and debugging purposes.

Author: LE GOURRIEREC Titouan
"""

############################################################################################################

import logging
import numpy as np

from data_analysis import generate_diff_dataframes
from data_utils import twitter_message
from file_operations import sync_folders
from twitter_utils import authenticate_twitter, post_tweet

logging.basicConfig(filename='log/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

############################################################################################################
################################              Main function              ###################################
############################################################################################################

def main():
    # Authenticate with Twitter
    client, api = authenticate_twitter()
    logging.info("Authenticated with Twitter.")

    # Load the data
    df = generate_diff_dataframes()
    logging.info("Data loaded.")

    # Generate the tweet message
    messages = twitter_message(df)
    logging.info(f"{len(messages)} Tweet messages generated.")

    # Post the tweets
    memory = np.load("log/memory.npy").tolist()
    for message in messages:
        response = post_tweet(client, api, message)

        memory.append(response.data['id'])
    np.save("log/memory.npy", memory)

    sync_folders()
    logging.info("Folders synced. data/data_after files moved to data/data_before and cleared.")
    logging.info("Script completed. \n\n --- \n")

if __name__ == "__main__":
    main()