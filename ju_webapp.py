from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import sys
import jinja2
import PLYex
import ju_webapp_parser
import os


app = Flask(__name__)
app.secret_key = "JURules"
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/interpreter", methods=["GET"])
def get_intext():
    # flash("get")
    return render_template("index.html")

@app.route("/interpreter", methods=["POST"])
def post_intext():
    # # Get input data from user
    intext = request.form['intext']
    intext = intext.encode('utf-8')

    # # Remove old test.ju file and write new data from user to file
    # os.remove("test.ju")
    with open("test.ju","w") as f:
        f.write(intext)

    # # Pass test.ju file to lexer and parser for evaluation to test.out file
    ju_webapp_parser.main()

    # # Read in evaluated code and flash to screen
    with open("test.out", "r") as fout:
        outtext=fout.readlines()

    # # for displaying intext back to screen
    with open("test.ju") as inf:
        infile = inf.readlines()

    flash("Congrats! Your input JU code was evaluated successfully!")

    return render_template("eval.html", outtext=outtext, intext = infile)

# @app.route("/about")
# def show_signup():
#     return render_template("about.html")


if __name__ == "__main__":
    app.run(debug = True)