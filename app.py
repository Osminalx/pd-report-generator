from flask import Flask, render_template, request, send_file
import pandas as pd
import os

from pd_report_gen import (
    generate_aluminum_df,
    generate_navel_df,
    generate_orders_df,
    generate_vulcan_df,
)

app = Flask(__name__)

orders_file = "./Archivos/ORDENES AZTEC SMI 2024.xlsm"
orders_sheet = "ORDENES"
vulc_sheet = "VULCANIZADO"

alumn_files = [
    (
        "./Archivos/LAMINAS GALVANIZADOS RELACION DE SCRAP EN CONTENEDORES METAL-HULE.xlsm",
        "RELACION GALVANIZADO",
    ),
    (
        "./Archivos/LAMINAS ALUMINIOS RELACION DE SCRAP EN CONTENEDORES METAL-HULE.xlsm",
        "RELACION ALUMINIO",
    ),
    (
        "./Archivos/LAMINAS STAINLESS RELACION DE SCRAP EN CONTENEDORES METAL-HULE.xlsm",
        "RELACION STAINLESS",
    ),
]

navel_files = [
    (
        "./Archivos/OMBLIGOS ALUMINIOS RELACION DE SCRAP EN CONTENEDORES METAL-HULE.xlsm",
        "RELACION ALUMINIO",
    ),
    (
        "./Archivos/OMBLIGOS GALVANIZADOS RELACION DE SCRAP EN CONTENEDORES METAL-HULE.xlsm",
        "RELACION GALVANIZADO",
    ),
]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_date_str = request.form["start_date"]
        end_date_str = request.form["end_date"]

        filename = f"reporte_{start_date_str}_to_{end_date_str}.xlsx"
        filepath = os.path.join("reportes_generados", filename)

        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)

        start_date = pd.to_datetime(start_date_str).date()
        end_date = pd.to_datetime(end_date_str).date()

        # Generate filtered dfs
        orders_df = generate_orders_df(orders_file, orders_sheet)
        vulcan_df = generate_vulcan_df(orders_file, vulc_sheet, start_date, end_date)
        aluminum_df = generate_aluminum_df(alumn_files, start_date, end_date)
        navel_df = generate_navel_df(navel_files, start_date, end_date)

        orders_df = orders_df.rename(columns={"DATE": "ORDER_DATE"})

        # Realizar el merge usando ORDER_ID
        merged_df = orders_df.merge(
            vulcan_df.merge(
                aluminum_df.merge(navel_df, on=["ORDER_ID", "DATE"], how="left"),
                on=["ORDER_ID", "DATE"],
                how="left",
            )
        )

        group_cols = [
            "STATUS",
            "ORDER_ID",
            "ORDER_DATE",
            "CUSTOMER",
            "SHEETS ORDER",
            "DATE",
            "QTY_TOTAL_VULCANIZADO",
        ]

        merged_df = merged_df.groupby(group_cols, as_index=False).agg(
            {
                "SCRAP_LAMINAS": lambda x: x.dropna().iloc[0]
                if not x.dropna().empty
                else pd.NA,
                "SCRAP_OMBLIGO_RONDANAS": lambda x: x.dropna().iloc[0]
                if not x.dropna().empty
                else pd.NA,
            }
        )

        merged_df.fillna("---", inplace=True)

        merged_df = merged_df.sort_values(["ORDER_ID", "DATE"])

        def replace_consecutive_duplicates(group):
            group["SCRAP_LAMINAS"] = group["SCRAP_LAMINAS"].where(
                group["SCRAP_LAMINAS"] != group["SCRAP_LAMINAS"].shift(), ""
            )
            group["SCRAP_OMBLIGO_RONDANAS"] = group["SCRAP_OMBLIGO_RONDANAS"].where(
                group["SCRAP_OMBLIGO_RONDANAS"]
                != group["SCRAP_OMBLIGO_RONDANAS"].shift(),
                "",
            )
            return group

        merged_df = merged_df.groupby("ORDER_ID", group_keys=False).apply(
            replace_consecutive_duplicates
        )

        # Custom name for each archive based on the dates
        filepath = os.path.join("reportes_generados", filename)

        # Save the filtered df to excel
        os.makedirs("reportes_generados", exist_ok=True)
        merged_df.to_excel(filepath, index=False)

        return send_file(filepath, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
