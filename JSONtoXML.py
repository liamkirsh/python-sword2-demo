#!/usr/bin/python

import sys
from jinja2 import Environment, PackageLoader
import json
from pprint import pprint

TEMPLATE = 'default.xml'

def main(inp):
    with open(inp, "r") as jsn:
        data = json.load(jsn)
        #import ipdb; ipdb.set_trace()
        #pprint(data)
        env = Environment(loader = PackageLoader('JSONtoXML', 'templates'))
        template = env.get_template(TEMPLATE)
        full_names = [author['full_name']
                      for author in data['metadata']['authors']]
        authors = [{'last': name.split(",")[0].strip(),
                    'first': name.split(",")[1].strip()}
                    for name in full_names]
        title = data['metadata']['titles'][0]['title'] 
        doi = data['metadata']['dois'][0]['value'] 
        pub_info = data['metadata']['publication_info'][0]
        publication = {'name': pub_info['journal_title'],
                       'year': pub_info['year'],
                       'volume': pub_info['journal_volume'], 
                       'issue': pub_info['journal_issue'],
                       'pp': pub_info['page_artid']}
        #print full_names, title, doi
        print template.render(title=title, doi=doi, authors=authors, publication=publication)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.stderr.write("ERROR: Must pass path to JSON as cmdline arg\n")
        sys.exit(1)
