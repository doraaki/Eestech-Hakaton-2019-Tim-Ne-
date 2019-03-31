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
    return "The current air pressure is {} Pa.".format(query.get_value('press')[1])

@app.route("/temp_data")
def temp_data():
    return "The current temperature is {} degrees celsius.".format(query.get_value('temp')[1])

@app.route("/pritisak")
def pritisak():
    return render_template("pressure.html")

@app.route("/press_graph")
def press_graph():
    print('dosao')
    query.make_graph('press')
    print('prosao')
    return render_template("pressure_graph.html")

@app.route('/plot.png')
def plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    
    data = query.get_graph('press')
    ys = data[1]
    print(data[1])
    #xs = range(len(ys))
    xs = data[0]
    #if(len(xs) > 2):
        #plt.xticks([xs[0], xs[-1]], visible=True, rotation="horizontal")
    axis.plot(xs, ys)
    fig.suptitle('PressureGraph', fontsize=12)
    axis.set_xlabel('time', fontsize=10)
    axis.set_ylabel('Pressure[Pa]', fontsize='medium')
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
@app.route('/plot1.png')
def plot1():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    
    data = query.get_graph('temp')
    ys = data[1]
    print(data[1])
    #xs = range(len(ys))
    xs = data[0]
    axis.plot(xs, ys)
    fig.suptitle('TemperatureGraph', fontsize=12)
    axis.set_xlabel('time', fontsize=10)
    axis.set_ylabel('Temp[C]', fontsize='medium')
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
@app.route("/temp_graph")
def temp_graph():
    query.make_graph('temp')
    return render_template("temperature_graph.html")

if __name__ == "__main__":
    app.run(debug=True)
