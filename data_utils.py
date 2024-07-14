"""
This module contains helper functions related to data manipulation and analysis for the World Athletics Records project.
It includes functions for converting country codes to flag emojis and generating Twitter-appropriate messages from DataFrames
that contain differences in sports records.

Functions:
- country_code_to_flag_emoji(country_code): Converts an ISO 3166-1 alpha-2 country code into the corresponding flag emoji.
- twitter_message(dataframe): Generates messages for Twitter from a DataFrame containing differences in sports records.

Author: LE GOURRIEREC Titouan
"""

############################################################################################################

import logging

import pandas as pd
import pycountry

logging.basicConfig(filename='log/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

############################################################################################################

def country_code_to_flag_emoji(country_code_alpha3: str) -> str:
    """
    Converts country codes to their corresponding flag emoji.

    Parameters:
        - country_code_alpha3 (str): The alpha-3 country code.
    
    Returns:
        - str: The flag emoji corresponding to the country code.
    
    Note:
        This function uses the pycountry library to get the country name from the alpha-3 code and then converts the alpha-2 code to
        the flag emoji using the Unicode Regional Indicator Symbols.
    """
    try:
        # get country by alpha-3 code
        country = pycountry.countries.get(alpha_3=country_code_alpha3.upper())
        # convert alpha-2 code to flag emoji
        return ''.join(chr(0x1F1E6 + ord(letter) - ord('A')) for letter in country.alpha_2)
    except AttributeError:
        return ''


def twitter_message(df: pd.DataFrame) -> str:
    """
    Generates a list of messages for Twitter based on the differences in sports records between two data points.

    This function iterates through a DataFrame where each row represents a comparison between an old and a new record
    in various sports disciplines. For each row, it constructs a message highlighting the new record, the discipline,
    the category, and the sex associated with the record, along with the performance details of the new and old records.
    It uses emojis to make the message more engaging.

    Parameters:
        - df (pd.DataFrame): A DataFrame containing columns for discipline, sex, category, and performance metrics
                           ('COMPETITOR_after', 'PERF_after', 'COUNTRY_after', 'VENUE_after', 'DATE_after',
                           'COMPETITOR_before', 'PERF_before', 'COUNTRY_before', 'VENUE_before', 'DATE_before').

    Returns:
        list: A list of strings, each string is a formatted message ready to be posted on Twitter.
    """
    messages = []
    
    for row in df.iterrows():
        discipline = row[1]["DISCIPLINE"]
        sex = row[1]["SEX"]
        category = row[1]["CATEGORY"]

        new_competitor = row[1]["COMPETITOR_after"]
        new_perf = row[1]["PERF_after"]
        new_country = row[1]["COUNTRY_after"]
        new_venue = row[1]["VENUE_after"]
        new_date = row[1]["DATE_after"]

        old_competitor = row[1]["COMPETITOR_before"]
        old_perf = row[1]["PERF_before"]
        old_country = row[1]["COUNTRY_before"]
        old_venue = row[1]["VENUE_before"]
        old_date = row[1]["DATE_before"]

        message = f"🚨 New {discipline} {sex} {category.replace("_", " ")} Record Alert! 🚨\n"
        message += f"🌟 {new_competitor} ({country_code_to_flag_emoji(old_country)}) shatters the record with a performance of {new_perf} 🏆 in {new_venue}, {new_date}.\n"
        message += f"👏 Previous record: {old_competitor} ({country_code_to_flag_emoji(old_country)}) - {old_perf} in {old_venue}, {old_date}."

    messages.append(message)

    return messages