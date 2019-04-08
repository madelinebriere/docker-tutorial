#!/bin/bash
rm -rf data 2> /dev/null
mkdir data
cd data && wget http://data.githubarchive.org/2015-01-01-{0..23}.json.gz