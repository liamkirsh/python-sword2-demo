#!/usr/bin/python

from sword2 import *
import logging

SD_URI = "http://localhost:8080/sd-uri"
user = "sword"
pw = "sword"

def main():
    logging.basicConfig() # NSA is watching
    c = Connection(SD_URI, user_name=user, user_pass=pw)

    #import ipdb; ipdb.set_trace()

    c.get_service_document()
    assert c.sd != None and c.sd.parsed and c.sd.valid

    print len(c.workspaces)
    print "workspaces", c.workspaces
    print "workspace 1 collections", c.workspaces[0][0]
    workspace_1_title, workspace_1_collections = c.workspaces[0]
    collection = workspace_1_collections[0]

    return

    #print collection # get a human-readable report for it

    with open("foo.jpg", "rb") as data:
        # docs are outdated: create replaced create_resource
        receipt = c.create(col_iri = collection.href,
                                    payload = data,
                                    mimetype = "application/zip",
                                    filename = "foo.jpg",
                                    packaging = "http://purl.org/net/sword/package/Binary")
    #print "\n\n\n" + str(receipt)

    e = Entry(id = "atomid",
                title = "atom title")
    #receipt2 = c.create(col_iri = collection.href,
    #                    metadata_entry = e)
    e.add_fields(dcterms_title = "dcterms title", dcterms_some_other_field = "other") 
    e.add_fields(author={"name":"Ben", "email":"foo@example.org"})
    print str(e)
    e.register_namespace("myschema", "http://example.org")
    e.add_fields(myscema_foo = "bar")
    receipt2 = c.create(col_iri = collection.href, metadata_entry = e)

if __name__ == '__main__':
    main()
