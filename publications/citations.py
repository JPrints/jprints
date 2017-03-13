
from citeproc.py2compat import *
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON

import json


available_styles = [ 'harvard1', 'acta-naturae', 'american-chemical-society', 'biomed-central']
def get_styles():
    return available_styles

orig_json_input = """
[
    {
        "id": "ITEM-1",
        "issued": {
            "date-parts": [[1987,  8,  3],
                           [2003, 10, 23]]
        },
        "title": "Ignore me",
        "type": "book"
    },
    {
      "id" : "ITEM-2",
      "page" : "1-7",
      "type" : "article-journal",
      "issued" : {
        "date-parts": [[2006]]
      }
    },
    {
        "author": [
            {
                "family": "Doe",
                "given": "John"
            }
        ],
        "id": "ITEM-3",
        "issued": {
            "date-parts": [["1965", "6", "1"]]
        },
        "title": "His Anonymous Life",
        "type": "book"
    },
    {
        "author": [
            {
                "family": "Grignon",
                "given": "Cyril"
            },
                        {
                "family": "Sentenac",
                "given": "Corey"
            }
        ],
        "id": "ITEM-4",
        "issued": {
            "date-parts": [[2000]]
       },
        "type": "book"
    },
    {
        "id": "ITEM-5",
        "title":"Boundaries of Dissent: Protest and State Power in the Media Age",
        "author": [
                {
                        "family": "D'Arcus",
                        "given": "Bruce"
                }
        ],
        "publisher": "Routledge",
        "publisher-place": "New York",
        "issued": {
            "date-parts":[[2006]]
        },
        "type": "book",
        "URL": "http://www.test01.com"
    }
]
"""


json_input = """
[
    {
        "id": "ITEM-5",
        "title":"Boundaries of Dissent: Protest and State Power in the Media Age",
        "author": [
                {
                        "family": "D'Arcus",
                        "given": "Bruce"
                }
        ],
        "publisher": "Routledge",
        "publisher-place": "New York",
        "issued": {
            "date-parts":[[2006]]
        },
        "type": "book",
        "URL": "http://www.test01.com"
    }
]
"""

def warn(citation_item):
    print("WARNING: Reference with key '{}' not found in the bibliography."
          .format(citation_item.key))

def form_bibliography( cit_style, input_data, id_list ):
    json_data = json.loads(input_data)
    bib_source = CiteProcJSON(json_data)

    bib_style = CitationStylesStyle(cit_style, validate=False)

    bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.html)
    for id in id_list:
        citation = Citation([CitationItem(id)])
        bibliography.register(citation)

    return bibliography.bibliography()


def testcitation():
    json_data = json.loads(json_input)
    bib_source = CiteProcJSON(json_data)

    #bib_style = CitationStylesStyle('harvard1', validate=False)
    #bib_style = CitationStylesStyle('acta-naturae', validate=False)
    #bib_style = CitationStylesStyle('american-chemical-society', validate=False)
    bib_style = CitationStylesStyle('biomed-central', validate=False)

    bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.html)
    #citation1 = Citation([CitationItem('ITEM-3')])
    #citation2 = Citation([CitationItem('ITEM-1'), CitationItem('ITEM-2')])
    #citation3 = Citation([CitationItem('ITEM-4')])
    citation4 = Citation([CitationItem('ITEM-5')])
    #citation5 = Citation([CitationItem('MISSING')])


    #bibliography.register(citation1)
    #bibliography.register(citation2)
    #bibliography.register(citation3)
    bibliography.register(citation4)
    #bibliography.register(citation5)


    print('Citations')
    print('---------')
    #print(bibliography.cite(citation1, warn))
    #print(bibliography.cite(citation2, warn))
    #print(bibliography.cite(citation3, warn))
    print(bibliography.cite(citation4, warn))
    #print(bibliography.cite(citation5, warn))

    print('')
    print('Bibliography')
    print('------------')

    for item in bibliography.bibliography():
        print(str(item))






