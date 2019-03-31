import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import io
import time
import sys
sys.path
sys.path.append('..')
import query
from flask import Flask, render_template, make_response

last_time = time.time()
curr_time = 0
query.make_graph('press')
query.make_graph('temp')
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/temperatura")
def temperatura():
    return render_template("temperature.html")


@app.route("/press_data")
def press_data():
    return "Trenutni pritisak je {} paskala.".format(query.get_value('press'))

@app.route("/temp_data")
def temp_data():
    return "Trenutna temperatura je {} stepeni.".format(query.get_value('temp'))

@app.route("/pritisak")
def pritisak():
    return render_template("pressure.html")

@app.route("/press_graph")
def press_graph():
    return render_template("pressure_graph.html")

@app.route('/plot.png')
def plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route("/temp_graph")
def temp_graph():
    #query.make_graph('temp')
    return render_template("temperature_graph.html")

if __name__ == "__main__":
    app.run(debug=True)
