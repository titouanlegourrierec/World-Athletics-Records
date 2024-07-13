import pandas as pd

def generate_diff_dataframes():
    """
    Generates a DataFrame containing differences between 'before' and 'after' records for each sex and category combination.

    Parameters:
    - sex_categories: List of sexes (e.g., ['men', 'women']).
    - record_categories: List of record categories (e.g., ['world', 'olympic']).
    - data_before_folder: Folder path containing 'before' records.
    - data_after_folder: Folder path containing 'after' records.

    Returns:
    - A DataFrame containing all differences with additional 'SEX' and 'CATEGORY' columns.
    """

    sex_categories = ['men', 'women']
    record_categories = ['world', 'olympic_games', 'african', 'asian', 'european', 'nacac', 'oceanian', 'south_american']

    data_diff_global = pd.DataFrame()

    for s in sex_categories:
        for c in record_categories:
            file_name_before = f'data_before_1/{s}_{c}_records.csv'
            file_name_after = f'data_after_1/{s}_{c}_records.csv'
            
            data_before = pd.read_csv(file_name_before)
            data_after = pd.read_csv(file_name_after)
            
            data_diff = pd.DataFrame()
            
            for discipline in data_before["DISCIPLINE"].unique():
                row_data_before = data_before[data_before["DISCIPLINE"] == discipline]
                row_data_after = data_after[data_after["DISCIPLINE"] == discipline]
                
                if not row_data_before.equals(row_data_after):
                    merged_row = pd.merge(row_data_before, row_data_after, on="DISCIPLINE", how="outer", suffixes=('_before', '_after'))
                    merged_row['SEX'] = s
                    merged_row['CATEGORY'] = c
                    data_diff = pd.concat([data_diff, merged_row], ignore_index=True)
            
            data_diff_global = pd.concat([data_diff_global, data_diff], ignore_index=True)
    
    return data_diff_global

