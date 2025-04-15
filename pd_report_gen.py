from datetime import date

import pandas as pd


def generate_orders_df(file: str, sheet: str) -> pd.DataFrame:
    # Orders df
    orders_df = pd.read_excel(
        file, sheet_name=sheet, header=None, skiprows=1, engine="openpyxl"
    )

    orders_columns = [0, 1, 2, 3, 10]

    orders_df = orders_df.iloc[:, orders_columns]

    orders_df.columns = ["STATUS", "ORDER_ID", "DATE", "CUSTOMER", "SHEETS ORDER"]

    orders_df["DATE"] = pd.to_datetime(orders_df["DATE"], errors="coerce").dt.date

    orders_df = orders_df[orders_df["DATE"].notna()]
    return orders_df


def generate_vulcan_df(
    file: str, sheet: str, start_date: date, end_date: date
) -> pd.DataFrame:
    # Vulcanized df
    vulcan_df = pd.read_excel(file, sheet_name=sheet, engine="openpyxl")

    vulc_columns = ["DATE", "JOB", "QTY TOTAL VULCANIZADO"]

    vulcan_df = vulcan_df.loc[:, vulc_columns]

    vulcan_df.columns = ["DATE", "ORDER_ID", "QTY_TOTAL_VULCANIZADO"]

    vulcan_df["DATE"] = pd.to_datetime(vulcan_df["DATE"], errors="coerce").dt.date

    vulcan_df = vulcan_df[vulcan_df["DATE"].notna()]

    start_date_dt = pd.to_datetime(start_date).date()
    end_date_dt = pd.to_datetime(end_date).date()

    mask = (vulcan_df["DATE"] >= start_date_dt) & (vulcan_df["DATE"] <= end_date_dt)

    return vulcan_df[mask]


def generate_aluminum_df(
    files: list[tuple[str, str]], start_date: date, end_date: date
) -> pd.DataFrame:
    dataframes = []
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()

    for file, sheet in files:
        df = pd.read_excel(file, sheet_name=sheet, header=9, engine="openpyxl")
        df = df[["Fecha", "# de Orden", "SCRAP/SHT"]]
        df.columns = ["DATE", "ORDER_ID", "SCRAP_LAMINAS"]

        # Convertir y filtrar
        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce").dt.date
        df = df[pd.notna(df["DATE"])]
        df = df[(df["DATE"] >= start_date) & (df["DATE"] <= end_date)]

        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    combined_df = combined_df.groupby(["ORDER_ID", "DATE"], as_index=False)[
        "SCRAP_LAMINAS"
    ].sum()

    return combined_df


def generate_navel_df(
    files: list[tuple[str, str]], start_date: date, end_date: date
) -> pd.DataFrame:
    dataframes = []
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()

    for file, sheet in files:
        df = pd.read_excel(file, sheet_name=sheet, header=9, engine="openpyxl")
        df = df.iloc[:, [1, 2, 18]]
        df.columns = ["DATE", "ORDER_ID", "SCRAP_OMBLIGO_RONDANAS"]

        # Convertir y filtrar
        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce").dt.date
        df = df[df["DATE"].notna()]
        df = df[(df["DATE"] >= start_date) & (df["DATE"] <= end_date)]

        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df = combined_df.groupby(["ORDER_ID", "DATE"], as_index=False)[
        "SCRAP_OMBLIGO_RONDANAS"
    ].sum()

    return combined_df

