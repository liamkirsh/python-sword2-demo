#!/usr/bin/python

from jinja2 import Environment, PackageLoader
import json

TEMPLATE = 'default.xml'


def convert_to_HAL(input_filename):
    with open(input_filename, "r") as jsn:
        data = json.load(jsn)

        env = Environment(loader=PackageLoader('convert_to_HAL', 'templates'))
        template = env.get_template(TEMPLATE)
        authors = [author for author in data['metadata']['authors']]
        authors = [{'last': author['full_name'].split(",")[0].strip(),
                    'first': author['full_name'].split(",")[1].strip(),
                    'affiliation_id': author['affiliations'][0]['recid']}
                   for author in data['metadata']['authors']]
        title = data['metadata']['titles'][0]['title']
        doi = data['metadata']['dois'][0]['value']
        pub_info = data['metadata']['publication_info'][0]
        publication = {'name': pub_info['journal_title'],
                       'year': pub_info['year'],
                       'volume': pub_info['journal_volume'],
                       'issue': pub_info['journal_issue'],
                       'pp': pub_info['page_artid']}
        structures = []
        for author in authors:
            structures.append({'recid': author['affiliation_id']})

        print template.render(title=title, doi=doi, authors=authors,
                              publication=publication, structures=structures)
