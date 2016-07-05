#!/usr/bin/python

from jinja2 import Environment, PackageLoader
import json

TEMPLATE = 'default.xml'
#from inspirehep.utils.record_getter import get_es_record
from inspirehep.modules.records.json_ref_loader import replace_refs
import sys


def convert_to_HAL(input_filename):
    with open(input_filename, "r") as jsn:
        data = json.load(jsn)

        env = Environment(loader=PackageLoader('inspirehep.modules.converttohal', 'templates'))
        template = env.get_template(TEMPLATE)
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

        my_affiliations = []
        recids = []
        structures = []
        for author in data['metadata']['authors']:
            for affiliation in author['affiliations']:
                if affiliation['recid'] not in recids:
                    my_affiliations.append(affiliation)
                    recids.append(affiliation['recid'])
        for affiliation in my_affiliations:
            sys.stderr.write(str(affiliation['record']) + "\n")
            ref = replace_refs(affiliation, 'db')
            sys.stderr.write(str(ref['record']) + "\n")
            sys.stderr.write(str(ref['record']['institution']) + "\n")
            #sys.stderr.write(str(ref['record']['message']))

            structures.append({'name': ref['record']['institution'][0],
                            'address': ref['record']['address'][0]['original_address'],
                            'country': ref['record']['address'][0]['country_code'],
                            'recid': ref['record']['oai_pmh'][0]['id'].split(":")[-1]
                           })

        print template.render(title=title, doi=doi, authors=authors,
                              publication=publication, structures=structures)
