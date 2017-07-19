#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import json
from elasticsearch import Elasticsearch

reload(sys)
#sys.setdefaultencoding("utf8")

es = Elasticsearch(
    ['10.10.21.82'],
    port=9200
)


def get_request_time(index, uri):
    agg_json = {
        "request_time_count": {
          "range": {
            "field": "request_time",
            "ranges": [
              {
                "to": 0.01
              },
              {
                "from": 0.01,
                "to": 0.05
              },
              {
                "from": 0.05,
                "to": 0.1
              },

              {
                "from": 0.1,
                "to": 0.45
              },
              {
                "from": 0.45,
                "to": 0.5
              },
              {
                "from": 0.5
              }
            ]
          }
        }
    }


    #res = es.search(index="service1-search-2017.07.16",body={"query":{"match_all":{}},"aggs":agg_json})
    # use term to match is also ok
    #res = es.search(index=index,body={"query":{"term":{"uri.keyword":uri}},"aggs":agg_json})
    #must use uri.keyword to match data
    res = es.search(index=index, body={"query": {"match":{"uri":uri}}, "aggs": agg_json})

    #res = es.count(index="service1-search-2017.07.16",body={'query':{'match':{'uri':'/nr/nr_get_nid'}}})['count']
    for line in  res['aggregations']['request_time_count']['buckets']:
        print line['key'] ,'\t', line['doc_count']


get_request_time(sys.argv[1],sys.argv[2])
