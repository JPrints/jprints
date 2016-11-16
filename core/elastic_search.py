import json
import urllib

from datetime import datetime
from elasticsearch import Elasticsearch

def initialise_elastic_search():

    es = Elasticsearch()
    index_exists = es.indices.exists(index='jprints')
    if index_exists:
        res = es.indices.delete(index='jprints' )
        print( "delete elastic search index ", res)
    cres = es.indices.create(index='jprints', ignore=400)
    print("done created elastic search index", cres)

def run_query( query ):
    from publications.models import Publication
    from core.models import Person
    results = []
    es = Elasticsearch()
    
    print("elastic_search::run_query term: ["+query+"]")
    #res = es.search(index='jprints', body={"query": {"match_all": { }}})
    #res = es.search(index='jprints', body={"query": 
    #                {   "bool": {"must" :{ "query_string" :{ "query": query } } }},
    #                    "highlight":{"fields":{ "title" : {} }} 
    #                } )
    #"matched_fields" : [ "depositor", "status", "type", "pub_status", "title", "abstract", "subject", "division" ],
    #"type": "fvh"
    # "order": "score",
    res = es.search(index='jprints', 
                     body={ 
                            "query": { 
                                "bool" :{
                                    "should": [
                                        { "match": { "family": query } },
                                        { "match": { "given": query } },
                                        { "match": { "title": query } },
                                        { "match": { "abstract": query } }
                                    ]
                                } 
                            },
                            "highlight": {
                                "fields": { 
                                    "family": {}, 
                                    "given": {}, 
                                    "title": {}, 
                                    "abstract": {}
                                }
                            }
                        }   
                    )
    print("Got %d Hits:" % res['hits']['total'])

    for hit in res['hits']['hits']:
        #print("time: %(timestamp)s, depositor: %(depositor)s, title: %(title)s, abs: %(abstract)s" % hit["_source"])
        #print("HIGHLIGHT: abs: %(abstract)s, title: %(title)s" % hit["highlight"])
        hit_type = hit["_type"]
        source = hit["_source"]
        hit_id = hit["_id"]
        citation = "" 
        if (hit_type == "person"):
            obj = Person.objects.get(pk=hit_id)
            citation = obj.get_search_citation()
        elif (hit_type == "publication"):
            obj = Publication.objects.get(pk=hit_id)
            citation = obj.get_search_citation()

        highlight_title = ""
        highlight_abs = ""
        highlight_text = ""
        highlight_family = ""
        highlight_given = ""
        highlight = hit["highlight"]
        for key,value in highlight.items():
            #print("highlight key:", key, "val:", value)
            if key == "title":
                highlight_title = value
            elif key == "abstract":
                highlight_abs = value
            elif key == "text":
                highlight_text = value
            elif key == "family":
                highlight_family = value
            elif key == "given":
                highlight_given = value

        print("highlight_title:", highlight_title, "highlight_abs:", highlight_abs, "family", highlight_family, "given", highlight_given)

        #print("\n\n\ntime: " + source["timestamp"]+ "\n\n\n")
        results.append({
                    'highlight_t': highlight_title,
                    'highlight_a': highlight_abs,
                    'highlight_ft': highlight_text,
                    'highlight_f': highlight_family,
                    'highlight_g': highlight_given,
                    'id': hit_id,
                    'type': hit_type,
                    'citation': citation,
                    })
    #   print("index: "+ hit )
    #   print("index: "+ hit['_index'] )
    #   print("type: "+ hit{'_type'} )
    #   source =  hit{'_source'}
    #   print("depositor: "+ source[{'depositor'} )

    #print("elastic_search::run_query results: ["+'\n'.join(map(str, results))+"]")
    return results

def index_person( person ):
    es = Elasticsearch()
    #print( "index_person [%s] called" % person.id)
    doc = {
       'userid'  : person.user.id,
       'username'     : person.user.username,
       'given'     : person.user.first_name,
       'family'     : person.user.last_name,
       'd_title'     : person.disp_title,
       'd_given'     : person.disp_given,
       'd_family'     : person.disp_family,
       'orcid'     : person.orcid,
       'user_type'     : person.user_type,
       'dept'     : person.dept,
       'org'     : person.org,
       'addr'     : person.addr,
    }
    res = es.index( index='jprints', doc_type="person", id=person.id, body=doc ) 
    #print(res['created'])
 

def index_publication( publication ):
    es = Elasticsearch()
    #str = "index_publication [%s] [%s] called" % ( publication.id, publication.title )
    #print (str)
    doc = {
       'id'         : publication.id,
       'depositor'  : publication.depositor.id,
       'status'     : publication.status,
       'type'       : publication.publication_type,
       'pub_status' : publication.publication_status,
       'title'      : publication.title,
       'abstract'   : publication.abstract,
       'subject'    : publication.subject,
       'timestamp'  : datetime.now(),
    }
    res = es.index( index='jprints', doc_type="publication", id=publication.id, body=doc ) 
    #print("index created:", res['created'])

