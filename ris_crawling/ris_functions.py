""" Helper functions to crawl """

# from urllib2 import *
import urllib
import json
import os
import requests

def test_query(q_in, anamnesis, evaluation, problem, sdate, edate, modality):
    # report, result, in2, in3, in4, sdate, edate, modality
    # http://localhost:8983/solr/ris_crawler/select?fq=anamnese:Sturz&fq=fragestellung:Blutung&q=*:*&wt=json
    """ blu
    """
    core = 'http://localhost:8983/solr/ris_crawler/select?'
    rows_in = '50'
    rows_out = '&rows=' + rows_in
    if q_in != '*:*':
        q_out = '&q=*' + q_in + '*'
    else:
        q_out = '&q=' + q_in
    
    filter_query = ''
    if anamnesis:
        filter_query = filter_query + "&fq=" + anamnesis
    if evaluation:
        filter_query = filter_query + "&fq=" + evaluation
    if problem:
        filter_query = filter_query + "&fq=" + problem
    # unters_beginn = '&unters_beginn>=' + sdate + ' and ' + 'unters_beginn<=' + edate

    # # funktioniert so wit...
    # technik = ''
    # if modality:
    #     technik = '&technik=' + modality[0]
    #     if len(modality) > 1:
    #         for i in range(1,len(modality)):
    #             technik = technik + ',' + modality[i]
    
    # if technik:
    #     go_for_it = go_for_it + technik
    
    go_for_it = core + '&wt=json' + q_out + rows_out + filter_query
    # go_for_it = core + q_out + '&wt=json'
    print(go_for_it)
    res = requests.get(go_for_it)
    response = res.json()
    return response

def format_text(dict_in, h_dict):
    """ This function takes in an array of texts and returns the
        text with every instance of the search_word highlighted
    """
    for one_dict in dict_in:
        datum = one_dict['unters_beginn']
        datum = datum[5:17] + 'um ' + datum[-12:-7]
        one_dict['unters_beginn'] = datum
        for key, value in h_dict.items():
            if key in one_dict['id']:
                for key2, value2 in value.items():
                    one_dict[key2] = value2[0]
                    
                    # one_dict['unters_beginn'] = one

    return dict_in
