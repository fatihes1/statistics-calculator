from flask import Flask, render_template, redirect, url_for, request, flash
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics as s
import base64
from io import BytesIO
from matplotlib.figure import Figure

app = Flask(__name__)

def geometrik(self):
    geo = self[0]
    for i in range(1, len(self)):
        geo *= self[i]
    geo **= (1 / len(self))
    return geo


@app.route("/")
def main():
    return render_template("index.html")



@app.route("/calculate", methods = ['POST'])
def calculater():
    input_array = request.form.get("input_array")
    if input_array[-1] == "," or input_array == "":
        return render_template("error.html")
    else:
        # TODO: en sona virgül konulmuşsa onu silip işlem yapılmalı
        # current_array = input_array.split(',')
        current_array = input_array.split(',')
        try:
            numbers = [float(numeric) for numeric in current_array]
            data = np.array(numbers)
            pandas_series = pd.Series(data)
            # Tablo oluşturma dizinin görünümü
            """
            fig, ax = plt.subplots()
            pandas_series.plot()
            fig.savefig('graph.png')
            """
            fig = Figure()
            ax = fig.subplots()
            ax.title.set_text("Sayı Dizisinin Grafiği")
            ax.plot(pandas_series)
            buf = BytesIO()
            fig.savefig(buf, format = "png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")                
            try:
                h_mean = s.harmonic_mean(numbers)
            except:
                h_mean = " - "
            try:
                g_mean = s.geometric_mean(numbers)
            except:
                g_mean = " - "
            result = {
                "mean" : pandas_series.mean(),
                "mode" : pandas_series.mode()[0],
                "count" : pandas_series.count(),
                "sum" : pandas_series.sum(),
                "std" : pandas_series.std(),
                "max" : pandas_series.max(),
                "min" : pandas_series.min(),
                "median" : pandas_series.median(),
                "var" : pandas_series.var(),
                "g_mean" : g_mean,
                "h_mean" : h_mean,
                "data": data
            }
            return render_template("result.html", result = result)
        except:
            return render_template("error.html")



if __name__ == "__main__":
    app.run(debug=True)