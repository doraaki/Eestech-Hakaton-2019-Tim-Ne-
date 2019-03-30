from flask import Flask, render_template             

app = Flask(__name__)


@app.route("/")
def temperatura():
    return render_template("home.html")

@app.route("/temperatura")
def temperatura():
    return render_template("temperatura.html")


@app.route("/pritisak")
def pritisak():
    return render_template("pritisak.html")

if __name__ == "__main__":
    app.run(debug=True)
