from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# TODO: check if the route is correct
final_df = pd.read_csv("reporte.csv", parse_dates=["date"])


@app.route("/")
def index():
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        filtered_df = final_df[
            (final_df["date"] >= start_date) & (final_df["date"] <= end_date)
        ]

        # save filtered df to csv
        # BUG: better save it in excel format
        filtered_df.to_csv("reporte.csv", index=False)

        return render_template(
            "index.html",
            tables=[filtered_df.to_html()],
            titles=filtered_df.columns.values,
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
