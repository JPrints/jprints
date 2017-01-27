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
    cres = es.indices.create(index='jprints', ignore=400, 
        body=
        {
            "mappings" : {
                "publication" : {
                    "properties" : {
                        "title_en" : {
                            "type" : "string",
                            "analyzer": "english"
                        },
                        "title_de" : {
                            "include_in_all": 'false',
                            "type" : "string",
                            "analyzer": "german"
                        },
                        "abstract_en" : {
                            "type" : "string", 
                            "analyzer": "english"
                        },
                        "abstract_de" : {
                            "include_in_all": 'false',
                            "type" : "string", 
                            "analyzer": "german"
                        },
                        "depositor" : {
                            "type" : "long"
                        },
                        "id" : {
                            "type" : "long"
                        },
                        "pub_status" : {
                            "type" : "keyword",
                        },
                        "status" : {
                            "type" : "keyword",
                        },
                        "subject" : {
                            "type" : "keyword",
                        },
                        "timestamp" : {
                            "type" : "date",
                        },
                        "item_type" : {
                            "type" : "keyword",
                        },
                        "milestone" : {
                            "type" : "date",
                        },
 
                    }
                }
            }
        } )

    print("done created elastic search index", cres)


def run_filter( ftype, ffield, fval ):
    from publications.models import Publication, Document
    from core.models import Person
    results = []
    es = Elasticsearch()
    
    dsl = json.dumps({ 'query' : { 'bool': { 
                                    'filter': { 
                                        'bool': { 
                                            'must': [ 
                                                { 'term' : { ffield : fval } }, 
                                                { 'term' : { '_type': ftype } } 
                                            ] } } } }, 
                                'sort': { 'timestamp': { 'order': 'desc' } } })

    print( "about to run dsl["+dsl+"]");
    res = es.search(index='jprints', body=dsl)
    
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        hit_type = hit["_type"]
        print( "got hit type:", str(hit_type) )
        print( "got hit :", str(hit) )
        source = hit["_source"]
        hit_id = hit["_id"]
        if (hit_type == "person"):
            obj = Person.objects.get(pk=hit_id)
        elif (hit_type == "publication"):
            obj = Publication.objects.get(pk=hit_id)
        elif (hit_type == "fulltext"):
            obj = Document.objects.get(pk=hit_id)

        results.append({
                    'id': hit_id,
                    'type': hit_type,
                    'obj': obj,
                    })

    print("elastic_search::run_publication_filter results: ["+'\n'.join(map(str, results))+"]")
    return results

def run_agg_filter( ):
    from publications.models import Publication, Document
    from core.models import Person
    results = []
    es = Elasticsearch()
    
    dsl = json.dumps({ 'query' : { 'bool': { 'filter': { 'term' : { 'item_type': 'A' } } } }, 'sort': { 'timestamp': { 'order': 'desc' } } })
    print( "about to run dsl["+dsl+"]");
    res = es.search(index='jprints', body=dsl)
    
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        hit_type = hit["_type"]
        print( "got hit type:", str(hit_type) )
        print( "got hit :", str(hit) )
        source = hit["_source"]
        hit_id = hit["_id"]
        if (hit_type == "person"):
            obj = Person.objects.get(pk=hit_id)
        elif (hit_type == "publication"):
            obj = Publication.objects.get(pk=hit_id)
        elif (hit_type == "fulltext"):
            obj = Document.objects.get(pk=hit_id)

        results.append({
                    'id': hit_id,
                    'type': hit_type,
                    'obj': obj,
                    })

    print("elastic_search::run_publication_filter results: ["+'\n'.join(map(str, results))+"]")
    return results





def run_query( query ):
    from publications.models import Publication, Document
    from core.models import Person
    results = []
    es = Elasticsearch()
    
    #res = es.search(index='jprints', body={"query": {"match_all": { }}})
    res = es.search(index='jprints', 
                     body={ 
                            "query": { 
                                "bool" :{
                                    "should": [
                                        { "match": { "family": query } },
                                        { "match": { "given": query } },
                                        { "match": { "title": query } },
                                        { "match": { "abstract": query } },
                                        { "match": { "body": query } },
                                        { "match": { "milestone": query } },
                                        { "match": { "filename": query } },
                                        { "match": { "filedesc": query } }
                                    ]
                                } 
                            },
                            "highlight": {
                                "fields": { 
                                    "family": {}, 
                                    "given": {}, 
                                    "title": {}, 
                                    "abstract": {},
                                    "body": {},
                                    "filename": {},
                                    "filedesc": {},
                                }
                            }
                        }   
                    )
    print("Got %d Hits:" % res['hits']['total'])

    for hit in res['hits']['hits']:
        hit_type = hit["_type"]
        source = hit["_source"]
        hit_id = hit["_id"]
        if (hit_type == "person"):
            obj = Person.objects.get(pk=hit_id)
        elif (hit_type == "publication"):
            obj = Publication.objects.get(pk=hit_id)
        elif (hit_type == "fulltext"):
            obj = Document.objects.get(pk=hit_id)

        highlight_title = ""
        highlight_abs = ""
        highlight_text = ""
        highlight_family = ""
        highlight_given = ""
        highlight_body = ""
        highlight_filename = ""
        highlight_filedesc = ""
        highlight = hit["highlight"]
        for key,value in highlight.items():
            print("highlight key:", key, "val:", value)
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
            elif key == "body":
                highlight_body = value
            elif key == "filename":
                highlight_filename = value
            elif key == "filedesc":
                highlight_filedesc = value

        results.append({
                    'highlight_t': highlight_title,
                    'highlight_a': highlight_abs,
                    'highlight_ft': highlight_text,
                    'highlight_f': highlight_family,
                    'highlight_g': highlight_given,
                    'highlight_b': highlight_body,
                    'highlight_fn': highlight_filename,
                    'highlight_fd': highlight_filedesc,
                    'id': hit_id,
                    'type': hit_type,
                    'obj': obj,
                    })

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
    from publications.models import Publication, Document
    es = Elasticsearch()

    print("index_publication", "id", publication.id, "date",  publication.publication_date );

    milestone = "1900-01-01"
    if (publication.publication_date):
        milestone = publication.publication_date
    elif (publication.online_date):
        milestone = publication.online_date
    elif (publication.accept_date):
        milestone = publication.accept_date
    elif (publication.submit_date):
        milestone = publication.submit_date
    elif (publication.complete_date):
        milestone = publication.complete_date

    my_str = "index_publication [%s] [%s] milestone[%s] called" % ( publication.id, publication.title, str(milestone) )
    print (my_str)

    doc = {
       'id'         : publication.id,
       'depositor'  : publication.depositor.id,
       'status'     : publication.status,
       'item_type'  : publication.publication_type,
       'pub_status' : publication.publication_status,
       'title_en'   : publication.title,
       'title_de'   : publication.title,
       'abstract_en': publication.abstract,
       'abstract_de': publication.abstract,
       'subject'    : publication.subject,
       'milestone'  : str(milestone),
       'timestamp'  : datetime.now(),
    }
    res = es.index( index='jprints', doc_type="publication", id=publication.id, body=doc ) 

    print("index DOCS !!!!!!!!!!!!!!!!! for publication [", publication.id, "]")
    documents = Document.objects.filter(publication__id=publication.id)
    for fulltext in documents:
        the_text =  "A full text for Article 2 edited"
        index_id = str(publication.id) 
        index_id += "_"
        index_id += str(fulltext.id) 
        print("index id[",index_id,"] doc[", fulltext.id, "] name[", fulltext.filefield.name, "]")
        doc = {
            #'id'        : index_id,
            'id'        : 1000*publication.id,
            'body'      : the_text,
            'filename'  : fulltext.filefield.name,
            'filedesc'  : fulltext.description,
            'timestamp' : datetime.now(),
        }
        res = es.index( index='jprints', doc_type="fulltext", id=fulltext.id, body=doc ) 



