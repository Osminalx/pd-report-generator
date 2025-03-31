from flask import Flask, render_template, request, send_file
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


@app.route("/")
def index():
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        # Generate filtered dfs
        orders_df = generate_orders_df(orders_file, orders_sheet, start_date, end_date)
        vulcan_df = generate_vulcan_df(orders_file, vulc_sheet, start_date, end_date)
        aluminum_df = generate_aluminum_df(alumn_files, start_date, end_date)
        navel_df = generate_navel_df(navel_files, start_date, end_date)

        # Merge data
        merged_df = (
            orders_df.merge(vulcan_df, on=["DATE", "ORDER_ID"], how="left")
            .merge(aluminum_df, on=["DATE", "ORDER_ID"], how="left")
            .merge(navel_df, on=["DATE", "ORDER_ID"], how="left")
        )

        # Custom name for each archive based on the dates
        filename = f"reporte_{start_date}_to_{end_date}.xlsx"
        filepath = os.path.join("reportes_generados", filename)

        # Save the filtered df to excel
        os.makedirs("reportes_generados", exist_ok=True)
        merged_df.to_excel(filepath, index=False)

        return send_file(filepath, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
