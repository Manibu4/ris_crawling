""" This file contains the initialisation routines for the db
    and all the routines including some html file.
"""

from flask import Flask, request, redirect, url_for, render_template
from ris_crawling.ris_functions import test_query, format_text

blu = Flask(__name__)

@blu.route('/')
def main():
    """ Initialise the connection to the db
        Fetch all rows which are already stored and
        display the list of all names on the main page
    """
    return render_template('index.html')


@blu.route('/show_results', methods=['POST'])
def show_results():
    """ Search for matching reports in the database
        and display them nicely
    """
    report_up = request.form["report"]
    report_dn = request.form["result"]
    anamnesis = request.form["anamnesis"]
    evaluation = request.form["evaluation"]
    problem = request.form["problem"]
    sdate = request.form["sdate"]
    edate = request.form["edate"]
    modality = request.form.getlist("technik")

    if report_dn:
        report = report_dn
    else:
        report = report_up

    response = test_query(report, anamnesis, evaluation, problem, sdate, edate, modality)
    dicts = response['response']
    # highlighted_dicts = response['highlighting']
    # print(highlighted_dicts)
    dict_of_docs = dicts['docs']
    # dict_of_docs = format_text(dict_of_docs, highlighted_dicts)
    return render_template('results.html', items=dict_of_docs, search_word=report, num_of_results=len(dict_of_docs))