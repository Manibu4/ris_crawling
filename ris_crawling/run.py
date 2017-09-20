""" This file contains the initialisation routines for the db
    and all the routines including some html file.
"""

import datetime
from threading import Timer
from flask import Flask, request, render_template
from ris_crawling.ris_functions import test_query
from ris_crawling.down_and_upload import fetch_one_ris_file, upload_to_solr, get_list_for_upload

blu = Flask(__name__)

# 1) If necessary, check for defective files and fetch them again
# -> will overwrite files
# get_failed_files()

def daily_up():
    """ Fetch one ris file, upload it to solr and move it to the
        appropriate folder
    """
    # Routine for the daily upload
    date = datetime.datetime.now() - datetime.timedelta(days=4)
    day = date.strftime("%Y-%m-%d")
    print('parsing ' + day)
    day = fetch_one_ris_file(day)
    print('parsing ' + day)
    path = '/Users/manu/Documents/Github/ris_crawling/json_files/'
    upload_to_solr([day], path)
    print("tadaa")

the_now = datetime.datetime.today()
update_time = the_now.replace(day=the_now.day+1, hour=13, minute=57, second=30, microsecond=0)
delta_t = update_time-the_now
secs = delta_t.seconds + 1
print(secs, "seconds remaining to ris update")

t = Timer(secs, daily_up)
t.start()


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
    dict_of_docs = dicts['docs']
    return render_template('results.html', items=dict_of_docs, search_word=report, num_of_results=len(dict_of_docs))