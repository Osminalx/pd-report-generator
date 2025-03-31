import pandas as pd


def filter_by_date(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    df["DATE"] = pd.to_datetime(df["DATE"])
    return df[(df["DATE"] >= start_date) & (df["DATE"] <= end_date)]


def generate_orders_df(
    file: str, sheet: str, start_date: str, end_date: str
) -> pd.DataFrame:
    # Orders df
    orders_df = pd.read_excel(file, sheet_name=sheet, header=None)

    orders_columns = [0, 1, 2, 3, 10]

    orders_df = orders_df.iloc[:, orders_columns]

    orders_df.columns = ["STATUS", "ORDER_ID", "DATE", "CUSTOMER", "SHEETS ORDER"]

    return filter_by_date(orders_df, start_date, end_date)


def generate_vulcan_df(
    file: str, sheet: str, start_date: str, end_date: str
) -> pd.DataFrame:
    # Vulcanized df
    vulcan_df = pd.read_excel(file, sheet_name=sheet, header=None)

    vulc_columns = ["DATE", "JOB", "QTY TOTAL VULCANIZADO"]

    vulcan_df = vulcan_df.iloc[:, vulc_columns]

    vulcan_df.columns = ["DATE", "ORDER_ID", "QTY_TOTAL_VULCANIZADO"]

    return filter_by_date(vulcan_df, start_date, end_date)


def generate_aluminum_df(
    files: list[(str, str)], start_date: str, end_date: str
) -> pd.DataFrame:
    dataframes = []

    needed_columns = ["Fecha", "# de Orden", "SCRAP/SHT"]

    for file, sheet in files:
        df = pd.read_excel(file, sheet_name=sheet, header=9)

        df = df[needed_columns]

        df.columns = ["DATE", "ORDER_ID", "SCRAP_SHT_ALUMINUM"]

        dataframes.append(df)

    df_aluminum = pd.concat(dataframes, ignore_index=True)

    return filter_by_date(df_aluminum, start_date, end_date)


def generate_navel_df(
    files: list[(str, str)], start_date: str, end_date: str
) -> pd.DataFrame:
    dataframes = []

    needed_columns = [1, 2, 16]

    for file, sheet in files:
        df = pd.read_excel(file, sheet_name=sheet, header=9)

        df = df.iloc[:, needed_columns]

        df.columns = ["DATE", "ORDER_ID", "SCRAP_SHT_NAVEL"]

        dataframes.append(df)

    navel_df = pd.concat(dataframes, ignore_index=True)
    return filter_by_date(navel_df, start_date, end_date)