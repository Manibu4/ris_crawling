""" This file contains the routines to downlad the json files from
    the ris as well as the routines to upload these files to solr
"""

import datetime
import urllib
import os
from os import walk

def download_ris_files(start_date, end_date):
    """ Download ris reports in json format from server
        in the range [start_date, end_date] which is to be given as input
        then pull each file in the range with 'fetch_one_ris_file'
    """
    base = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    delta = datetime.timedelta(days=1)
    date = base - delta
    placeholder = date.strftime("%Y-%m-%d")

    while placeholder != end_date:
        date = date + delta
        placeholder = date.strftime("%Y-%m-%d")
        print 'parsing ' + placeholder
        fetch_one_ris_file(placeholder)


def fetch_one_ris_file(one_day):
    """ This function fetches one ris report for the day given as input
        Subsequently, the file is saved as json-file in the folder 'json_files'
    """
    filename = one_day + '-parsed.json'
    url = 'http://meqpacscrllt01.uhbs.ch:9000/q?day=' + one_day
    response = urllib.urlopen(url)
    data = response.read()
    file_path = 'json_files/' + filename

    if not os.path.exists(os.path.dirname(file_path)):
        os.mkdir(os.path.dirname(file_path))

    with open(file_path, "w") as my_file:
        my_file.write(data)
    return filename


def get_list_for_upload():
    """ This routine is able to go through a folder and collect a large list of
        names for a first large upload to solr. Finally, it uploads this list
    """
    my_path = '/Users/manu/Documents/Github/ris_crawling/json_files/'
    list_of_json_files = []
    for (_, _, filenames) in walk(my_path):
        list_of_json_files.extend(filenames)

    upload_to_solr(list_of_json_files, my_path)


def upload_to_solr(list_of_json_files, path):
    """ This function takes a list of json files in a particular folder
        i.e. "json_files" and uploads its contents to solr
        Finally, the file will be moved to the folder 'up', which contains
        all files that have been uploaded to solr
    """
    url = 'http://localhost:8983/solr/ris_crawler/update/json?stream.file='
    appendix = '&stream.contentType=text/plain;charset=utf-8'
    for one_file in list_of_json_files:
        go_for_it = url + path + one_file + appendix
        urllib.urlopen(go_for_it)
        print path + one_file
        os.rename(path + one_file, path + 'up/'+ one_file)


def get_failed_files():
    """ Fetch the files which were not downloaded completely upon request
    """
    path = '/Users/manu/Documents/Github/ris_crawling/json_files/up'

    failed = []
    for (_, _, filenames) in walk(path):
        for one_file in filenames:
            name = path + one_file
            size = os.path.getsize(name)
            if size < 200:
                print one_file
                failed.append(one_file[0:10])

    for element in failed:
        fetch_one_ris_file(element)
        print 'parsed ' + element
