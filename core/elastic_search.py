import json
import urllib
import re
import requests
from tika import parser
import base64

from datetime import datetime
from elasticsearch import Elasticsearch, NotFoundError
from django.utils.translation import get_language
from django.conf import settings


def initialise_pipeline():
    es = Elasticsearch()
    try:
        ingest = es.ingest.get_pipeline( [ "attachment" ])
        print("pipeline found: ", ingest)
        res = es.ingest.delete_pipeline( "attachment" )
        print("pipeline deleted: ", res)
    except NotFoundError:
        print("pipeline not found")

    res = es.ingest.put_pipeline( "attachment", 
        body = { 
            "description" : "Extract fulltext data",
            "processors" : [
                {
                      "attachment" : {
                              "field" : "data",
                              "target_field" : "attachment"
                      }
                }
            ]
    })
    print("pipeline created: ", res)


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
                        }
                    }
                },
                #"fulltext" : {
                #    "properties" : {
                #        "title" : {
                #            "type" : "text",
                #        },
                #        "thedata" : {
                #            "type" : "text",
                #        }
                #    }
                #},
                "person" : {
                    "properties" : {
                        "userid" : {
                            "type" : "long"
                        },
                        "username" : {
                            "type" : "keyword",
                        },
                        "given" : {
                            "type" : "string",
                        },
                        "family" : {
                            "type" : "string",
                        },
 
                        "d_given" : {
                            "type" : "string",
                        },
                        "d_family" : {
                            "type" : "string",
                        },
                        "orcid" : {
                            "type" : "keyword",
                        },
                        "user_type" : {
                            "type" : "keyword",
                        },
                        "dept" : {
                            "type" : "keyword",
                        },
                        "org" : {
                            "type" : "keyword",
                        },
                        "addr" : {
                            "type" : "string",
                        },
                        "first_char" : {
                            "type" : "keyword",
                        },
 
                    }
                },
            }
        } )

    print("done created elastic search index", cres)


def run_filter( ftype, ffield, fval ):
    from publications.models import Publication, Document
    from core.models import Person
    results = []
    es = Elasticsearch()
    print( "run_filter", ftype, ffield, fval )

    fterm1 ={ '_type': ftype } 
    term1 = { 'term' : fterm1 }
    fterm2 ={ ffield : fval } 
    term2 = { 'term' : fterm2 }
    must = { 'must' : [ term1, term2 ] }
    boolt = { 'bool': must }
    filtert = { 'filter': boolt }
    boolt2 = { 'bool': filtert }
    dslraw = { 'query': boolt2} 

    dsl = json.dumps( dslraw ) 

#    dsl = json.dumps({ 'query' : { 'bool': { 
#                                    'filter': { 
#                                        'bool': { 
#                                            'must': [ 
#                                                { 'term' : { ffield : fval } }, 
#                                                { 'term' : { '_type': ftype } } 
#                                            ] } } } }, 
#                                'sort': { 'timestamp': { 'order': 'desc' } } })

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

    print("elastic_search::run_filter results: ["+'\n'.join(map(str, results))+"]")
    return results

def run_agg_filter( ftype, query_from, query_size, filter_terms, milestone_terms ):
    from publications.models import Publication, Document
    from core.models import Person
    results = {} 
    es = Elasticsearch()
 
    sort_term = {}
    if ( ftype == "publication"):
        sort_term = { 'milestone': { 'order': 'asc' }}
    else:
        sort_term = { 'family': { 'order': 'asc' }}
    query = { 'bool': { 'filter': { 'term' : { '_type': ftype } } } }
    sort = { 'timestamp': { 'order': 'desc' } }
    aggs = {}
    if ( ftype == "publication"):
        aggs = {  
            "item_type": { "terms": { "field": "item_type" } }, 
            "pub_status": { "terms": { "field": "pub_status" } }, 
            "status"    : { "terms": { "field": "status" } }, 
            "milestone" : { "date_histogram": { "field" : "milestone", "interval" : "year", "format" : "yyyy"  } }, 
        } 
    elif ( ftype == "person"):
        aggs = {  
            "org" : { "terms": { "field": "org" } }, 
            "dept": { "terms": { "field": "dept" } }, 
            "user_type": { "terms": { "field": "user_type" } }, 
    #        "family"   : { "terms": { "field": "family" } }, 
            "first_char" : { "terms": { "field": "first_char" } }, 
        } 
    else:
        aggs = { }

    post_filter = { } 
    terms = []
    for pf in filter_terms:
        this_term = { 'term' : pf }
        terms.append(this_term)
    for pf in milestone_terms:
        this_term = { 'range' : pf }
        terms.append(this_term)


    # use a "should" term filter so that it is an "OR" rather than an "AND" that you would get with "must"
    #bool_terms = { 'must' : terms }
    bool_terms = { 'should' : terms }
    post_filter = { 'bool':  bool_terms } 


    dslraw = { 'from': query_from,
               'size': query_size,
               'sort': sort_term,
               'query': query, 
               'sort': sort, 
               'aggs': aggs,
               'post_filter': post_filter
             } 

    dsl = json.dumps( dslraw ) 

    print( "run_agg_filter about to run \n\ndsl["+dsl+"]", 'formed from\n\n', dslraw );
    res = es.search(index='jprints', body=dsl)
    
    the_hits = []
    the_total = res['hits']['total']
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

        the_hits.append({
                    'id': hit_id,
                    'type': hit_type,
                    'obj': obj,
                    })

    the_aggs = {}
    if 'aggregations' in res:
        for k,v in res['aggregations'].items():
            this_agg = {}
            for bucket in res['aggregations'][k]['buckets']:
                key_name = bucket['key']
                key_label = ""
                key_count = 0
                key_selected = 0
                if 'key_as_string' in bucket:
                    key_label = bucket['key_as_string']
                else:
                    key_label = get_bucket_key_str( k, bucket['key'] )

                if 'doc_count' in bucket:
                    key_count = bucket['doc_count']
                if is_key_selected( k, key_name, filter_terms, milestone_terms ):
                    key_selected = 1
                    print("found item")
                elif is_key_selected( k, key_label, filter_terms, milestone_terms ):
                    key_selected = 1
                    print("found item")

                this_agg[key_name] = {}
                this_agg[key_name]['count'] = key_count
                this_agg[key_name]['label'] = key_label
                this_agg[key_name]['selected'] = key_selected

            the_aggs[k] = this_agg
            #print("the aggs", the_aggs)
        
    results = { 
        'hits' : the_hits,
        'aggs' : the_aggs,
        'total': the_total
    }
    return results

def is_key_selected( term, key, selections, milestones ):
    if term == "milestone":
        year_match = re.match( "^\d\d\d\d$", str(key) )
        if year_match:
            for poss in milestones:
                year_term = str(key)+"||/y"
                if ( str(term) in poss ):
                    if str(year_term) in str(poss[term]):
                        return True
    else:
        for poss in selections:
            if ( term in poss ):
                if str(poss[term]) == str(key):
                    return True

    return False

def get_bucket_key_str( term, key ):
    from publications.models import Publication, Document
    key_str = key
    if ( term == "item_type" ):
        key_str = Publication.get_choice_disp_str( Publication.PUBLICATION_TYPES, key)
    elif ( term == "pub_status" ):
        key_str = Publication.get_choice_disp_str( Publication.PUBLICATION_STATES, key)
    elif ( term == "status" ):
        key_str = Publication.get_choice_disp_str( Publication.STATUS_TYPES, key)
    elif ( term == "milestone" ):
        key_str = key
    elif ( term == "org" ):
        key_str = key
    elif ( term == "dept" ):
        key_str = key
    elif ( term == "user_type" ):
        key_str = key
    elif ( term == "family" ):
        key_str = key
    elif ( term == "first_char" ):
        key_str = key
    return key_str

def run_query( query ):
    from publications.models import Publication, Document
    from core.models import Person
    results = []
    es = Elasticsearch()
    
    query_from = 0
    query_size = 10

    family_term = { 'match': { 'family' : query } }
    family_d_term = { 'match': { 'd_family' : query } }
    given_term  = { 'match': { 'given' : query } }
    given_d_term  = { 'match': { 'd_given' : query } }
    title_en_term  = { 'match': { 'title_en' : query } }
    title_de_term  = { 'match': { 'title_de' : query } }
    abstract_en_term  = { 'match': { 'abstract_en' : query } }
    abstract_de_term  = { 'match': { 'abstract_de' : query } }
    filename_term  = { 'match': { 'filename' : query } }
    filedesc_term  = { 'match': { 'filedesc' : query } }
    fulltext_term  = { 'match': { 'attachment.content' : query } }

    must_terms = {}
    should_terms = [
        family_term,
        family_d_term,
        given_term,
        given_d_term,
        filename_term,
        filedesc_term,
        fulltext_term,
    ] 
    current_lang = get_language()
    if not current_lang:
        current_lang = "en"

    if current_lang == "de":
        should_terms.append(title_de_term)
        should_terms.append(abstract_de_term)
    else:
        should_terms.append(title_en_term)
        should_terms.append(abstract_en_term)

    bool_terms = { 
                    'should' : should_terms,
                }

    query = { "bool": bool_terms }

    highlight_fields_en = { "family": {}, "family_d": {}, "given": {},"given_d": {}, 
                            "title_en": {}, "abstract_en": {}, 
                            "attachment.content": {}, "filename": {}, "filedesc": {}, }
    highlight_fields_de = { "family": {},"family_d": {}, "given": {}, "given_d": {}, 
                            "title_de": {}, "abstract_de": {}, 
                            "attachment.content": {}, "filename": {}, "filedesc": {}, }

    if current_lang == "de":
        highlight_fields = { "fields": highlight_fields_de }
    else:
        highlight_fields = { "fields": highlight_fields_en }

    dslraw = { 'from': query_from,
               'size': query_size,
               #'sort': sort_term,
               'query': query, 
               'highlight' : highlight_fields,
               #'sort': sort, 
               #'aggs': aggs,
               #'post_filter': post_filter
             } 

    dsl = json.dumps( dslraw ) 

    #print( "run_query about to run \n\ndsl["+dsl+"]", 'formed from\n\n', dslraw );
    res = es.search(index='jprints', body=dsl)

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
            id_match = re.match( "^(\d+)_(\d+)", str(hit_id) )
            if id_match:
                pub_id = id_match.group(1) 
                doc_id = id_match.group(2) 
                obj = Document.objects.get(pk=doc_id)
                hit_id = doc_id

        highlight_title = ""
        highlight_abs = ""
        highlight_family = ""
        highlight_given = ""
        highlight_fulltext = ""
        highlight_filename = ""
        highlight_filedesc = ""
        if 'highlight' in hit:
            highlight = hit["highlight"]
            for key,value in highlight.items():
                print("highlight key:", key, "val:", value)
                if key == "title_en":
                    highlight_title = value
                elif key == "title_de":
                    highlight_title = value
                elif key == "abstract_en":
                    highlight_abs = value
                elif key == "abstract_de":
                    highlight_abs = value
                elif key == "family":
                    highlight_family = value
                elif key == "family_d":
                    highlight_family = value
                elif key == "given":
                    highlight_given = value
                elif key == "given_d":
                    highlight_given = value
                elif key == "attachment.content":
                    highlight_fulltext = value
                elif key == "filename":
                    highlight_filename = value
                elif key == "filedesc":
                    highlight_filedesc = value

        results.append({
                    'highlight_t': highlight_title,
                    'highlight_a': highlight_abs,
                    'highlight_f': highlight_family,
                    'highlight_g': highlight_given,
                    'highlight_b': highlight_fulltext,
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
    family = ""
    first_char = ""
    if person.disp_family:
        family = person.disp_family
    elif person.user.last_name:
        family = person.user.last_name
    if len(family):
        family = family.capitalize()
        first_char = family[0]

    doc = {
       'userid'  : person.user.id,
       'username'     : person.user.username,
       'given'     : person.user.first_name,
       'family'     : person.user.last_name,
       'd_given'     : person.disp_given,
       'd_family'     : person.disp_family,
       'orcid'     : person.orcid,
       'user_type'     : person.user_type,
       'dept'     : person.dept,
       'org'     : person.org,
       'addr'     : person.addr,
       'first_char' : first_char,
    }
    res = es.index( index='jprints', doc_type="person", id=person.id, body=doc ) 
    #print(res['created'])
 
def rm_index_person( person ):
    es = Elasticsearch()
    #print( "rm_index_person called for id", person.id)
    res = es.delete( index='jprints', doc_type="person", id=person.id ) 
    #print(res)
 

def rm_index_publication( publication ):
    from publications.models import Publication, Document
    es = Elasticsearch()

    documents = Document.objects.filter(publication__id=publication.id)
    for fulltext in documents:
        if fulltext.filefield:
            ingest_id = str(publication.id)+'_'+str(fulltext.id)
            #print("rm_index_publicationi FULLTEXT ", "id", ingest_id );
            res = es.delete( index='jprints', doc_type="fulltext", id=ingest_id ) 
            #print(res)
 
    #print("rm_index_publication", "id", publication.id );
    res = es.delete( index='jprints', doc_type="publication", id=publication.id ) 
    #print(res)


def index_publication( publication ):
    from publications.models import Publication, Document
    es = Elasticsearch()

    #print("index_publication", "id", publication.id, "date",  publication.publication_date );

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

    documents = Document.objects.filter(publication__id=publication.id)
    for fulltext in documents:
        try:
            doc_path = settings.MEDIA_DIR + fulltext.filefield.name
            doc_text = parser.from_file(doc_path) 

            b64_text = base64.b64encode(doc_text['content'].encode("utf-8"))
            b64_ascii = str( b64_text, 'ascii' )
            ingest_body = { "data": b64_ascii }

            ingest_id = str(publication.id)+'_'+str(fulltext.id)
            ingest_url = 'http://localhost:9200/jprints/fulltext/'+ingest_id+'?pipeline=attachment'
            headers = { 'Content-Type': 'application/json' }
            ingest_res = requests.put( ingest_url, headers=headers, data=json.dumps(ingest_body) )

        except FileNotFoundError:
            print("File not found for ingest")




