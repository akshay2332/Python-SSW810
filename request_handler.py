"""
Module Request handler to handle all incoming requests from client.
"""

from flask import Flask, render_template
from utilities.HW11_Akshay_Rane import Instructor
from utilities.HW11_Akshay_Rane import Repository

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("homepage.html", page_title="Homepage")


@app.route("/instructor_summary")
def instructor_summary():
    """
    Function to display instructor summary form database
    :return: page to display instructor summary
    """
    stevens_repository = Repository("Stevens", None, False)

    return render_template("instructor_summary_view.html", instructors=stevens_repository.instructor_table_db(None),
                           table_header=Instructor.INSTRUCTORS_FIELDS, title="Instructors", table_title="Summary:",
                           page_title="Stevens Instructor Summary")


app.run(debug=True)
