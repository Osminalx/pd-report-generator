import pandas as pd
import glob

# HACK: execute before using the flask app

routes = [
    # TODO: add routes
]

# Needed columns from each route

columns_group_1 = ["JOB", "status", "sheets_order"]
columns_group_2 = ["JOB", "QTY", "total_vulcanizado", "date"]
columns_group_3 = ["JOB", "date", "scrap_sheets"]

# Read and combine the files
dataframes = []
for route, columns in zip(routes, [columns_group_1, columns_group_2, columns_group_3]):
    files = glob.glob(route)
    for file in files:
        df = pd.read_excel(file, usecols=columns)
        dataframes.append(df)

# combine all dfs into one
final_df = pd.concat(dataframes, ignore_index=True)
