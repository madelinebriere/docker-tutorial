#!/usr/bin/python

import os
import json
import gzip
import re
import collections

"""
Analysis script to run inside the Docker container.
"""

DATA_DIRECTORY = '/data'

def analyze_file(filename):
    word_frequencies = collections.defaultdict(lambda:0)
    with gzip.open(os.path.join(DATA_DIRECTORY,filename),'r') as input_file:
        for line in input_file:
            data = json.loads(line.decode('utf-8'))
            if data['type'] == 'PushEvent':
                for commit in data['payload']['commits']:
                    words = [word for word in re.compile('[^a-z\-\_]')\
                             .split(commit['message'].lower()) if word]
                    for word in words:
                        word_frequencies[word]+=1
    return word_frequencies

if __name__ == '__main__':
    input_filenames=os.environ['INPUT_FILENAMES'].split(';')
    for input_filename in input_filenames:
        output_filename = input_filename[:-3]#we cut away the .gz
        result=analyze_file(input_filename)
        print(json.dumps(result)+";;")
