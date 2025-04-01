import pandas as pd


def generate_orders_df(
    file: str, sheet: str, start_date: str, end_date: str
) -> pd.DataFrame:
    # Orders df
    orders_df = pd.read_excel(file, sheet_name=sheet, header=None, skiprows=1)

    orders_columns = [0, 1, 2, 3, 10]

    orders_df = orders_df.iloc[:, orders_columns]

    orders_df.columns = ["STATUS", "ORDER_ID", "DATE", "CUSTOMER", "SHEETS ORDER"]

    orders_df["DATE"] = pd.to_datetime(orders_df["DATE"], errors="coerce")

    orders_df = orders_df[orders_df["DATE"].notna()]

    mask = (orders_df["DATE"] >= pd.to_datetime(start_date)) & (
        orders_df["DATE"] <= pd.to_datetime(end_date)
    )

    return orders_df[mask]


def generate_vulcan_df(
    file: str, sheet: str, start_date: str, end_date: str
) -> pd.DataFrame:
    # Vulcanized df
    vulcan_df = pd.read_excel(file, sheet_name=sheet)

    vulc_columns = ["DATE", "JOB", "QTY TOTAL VULCANIZADO"]

    vulcan_df = vulcan_df.loc[:, vulc_columns]

    vulcan_df.columns = ["DATE", "ORDER_ID", "QTY_TOTAL_VULCANIZADO"]

    vulcan_df["DATE"] = pd.to_datetime(vulcan_df["DATE"], errors="coerce")

    vulcan_df = vulcan_df[vulcan_df["DATE"].notna()]

    mask = (vulcan_df["DATE"] >= pd.to_datetime(start_date)) & (
        vulcan_df["DATE"] <= pd.to_datetime(end_date)
    )

    return vulcan_df[mask]


def generate_aluminum_df(
    files: list[(str, str)], start_date: str, end_date: str
) -> pd.DataFrame:
    dataframes = []
    start_date = pd.to_datetime(start_date)  # Convertir una vez
    end_date = pd.to_datetime(end_date)

    for file, sheet in files:
        df = pd.read_excel(file, sheet_name=sheet, header=9)
        df = df[["Fecha", "# de Orden", "SCRAP/SHT"]]
        df.columns = ["DATE", "ORDER_ID", "SCRAP_SHT_ALUMINUM"]

        # Convertir y filtrar
        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
        df = df[df["DATE"].notna()]
        df = df[(df["DATE"] >= start_date) & (df["DATE"] <= end_date)]

        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)


def generate_navel_df(
    files: list[(str, str)], start_date: str, end_date: str
) -> pd.DataFrame:
    dataframes = []
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    for file, sheet in files:
        df = pd.read_excel(file, sheet_name=sheet, header=9)
        df = df.iloc[:, [1, 2, 16]]
        df.columns = ["DATE", "ORDER_ID", "SCRAP_SHT_NAVEL"]

        # Convertir y filtrar
        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
        df = df[df["DATE"].notna()]
        df = df[(df["DATE"] >= start_date) & (df["DATE"] <= end_date)]

        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)
