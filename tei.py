#!/usr/bin/python

from jinja2 import Environment, PackageLoader
import json

TEMPLATE = 'default.xml'
#from inspirehep.utils.record_getter import get_es_record
from inspirehep.modules.records.json_ref_loader import replace_refs
import sys


def tei_response(record):
    
    data = record
    env = Environment(loader=PackageLoader('inspirehep.modules.converttohal',
                                           'templates'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(TEMPLATE)
    #sys.stderr.write(str(data['authors'][0]['affiliations'][0]['recid']) + '\n')
    #import ipdb; ipdb.set_trace()

    if 'authors' in data:
        authors = []
        for author in data['authors']:
            # handle first/last name
            auth_spl = author['full_name'].split(",")
            if len(auth_spl) == 2:
                last = auth_spl[0].strip()
                first = auth_spl[1].strip()
            else:
                last = author['full_name']
                first = ""

            authors.append({'last': last,
                            'first': first,
                            'affiliation_id': author['affiliations'][0]['recid']
                                if 'recid' in author['affiliations'][0]
                                else ""
                           })
    else:
        authors = []

    title = data['titles'][0]['title']

    # TODO: update the following line
    doi = data['dois'][0]['value'] if 'dois' in data else ""

    if 'publication_info' in data:
        pub_info = data['publication_info'][0]
        if 'journal_title' in pub_info:
            if 'page_artid' in pub_info:
                pp = pub_info['page_artid']
            elif 'page_start' and 'page_end' in pub_info:
                pp = pub_info['page_start'] + "-" + pub_info['page_end']
            elif 'page_start' in pub_info or 'page_end' in pub_info:
                pp = pub_info['page_start'] or pub_info['page_end']
            else:
                pp = ""

            publication = {'type': "journal",
                           'name': pub_info['journal_title'],
                           'year': pub_info['year'],
                           'volume': pub_info['journal_volume']
                               if 'journal_volume' in pub_info
                               else "",
                           'issue': pub_info['journal_issue']
                               if 'journal_issue' in pub_info
                               else "",
                           'pp': pp}
        elif 'conference_record' in pub_info:
            publication = _conference_data(pub_info['conference_record'])
        else:
            publication = None
    else:
        publication = None

    my_affiliations = []
    recids = []
    structures = []
    if 'authors' in data:
        for author in data['authors']:
            for affiliation in author['affiliations']:
                if 'recid' in affiliation and affiliation['recid'] not in recids:
                    my_affiliations.append(affiliation)
                    recids.append(affiliation['recid'])
    for affiliation in my_affiliations:
        ref = replace_refs(affiliation, 'db')

        #import ipdb; ipdb.set_trace()
        #sys.stderr.write(str(ref) + '\n')
        #sys.stderr.write(str(ref['record']) + '\n')
        #sys.stderr.write(str(ref['record']['collections']) + '\n')
        #sys.stderr.write(str(ref['record']['collections'][1]['primary']) + '\n\n')
        if (ref['record']
                and 'collections' in ref['record']
                and ref['record']['collections']):
            structures.append({'type': ref['record']['collections'][1]['primary'].lower()
                                   if len(ref['record']['collections']) >= 2 else "",
                               'name': ref['record']['institution'][0],
                               'address': ref['record']['address'][0]['original_address'],
                               'country': ref['record']['address'][0]['country_code'],
                               'recid': ref['record']['oai_pmh'][0]['id'].split(":")[-1]
                              })

    print template.render(title=title, doi=doi, authors=authors,
                          publication=publication, structures=structures)

def _conference_data(conf_record):
    #sys.stderr.write(str(conf_record))
    ref = replace_refs(conf_record, 'db')
    #sys.stderr.write(str(ref))
    o_addr = ref['address'][0]['original_address'].split(" ")
    city = o_addr[0][:-1] # trim off comma
    country = o_addr[1]

    date = ref['date'].split(" ")
    month = date[1]
    year = date[2]

    return {'type': "conference",
            'name': ref['titles'][0]['title'],
            'acronym': ref['acronym'][0],
            'opening_date': ref['opening_date'],
            'closing_date': ref['closing_date'],
            'month': month,
            'year': year,
            'city': city,
            'country': country,
            'country_code': ref['address'][0]['country_code']}
