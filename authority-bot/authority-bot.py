#!/usr/bin/env python3

"""
   Bot script to take tsv results of Wikidata query for people with Open Library ids
   and VIAF or ISNI for writeback to OL.

"""
import sys
from olclient.openlibrary import OpenLibrary



if __name__ == '__main__':
    fname = sys.argv[1]
    ol = OpenLibrary()

    with open(fname, 'r') as f:
        for line in f.readlines():
            url, olid, viaf, isni = line.strip().split('\t')
            if url == 'item':
                continue 
            qnum = url.split('/')[4]
            isni = isni.replace(' ', '')
            #print("DEBUG", qnum, olid, viaf, isni)
            e = ol.get(olid)
            assert e.type.get('key') == '/type/author'
            ids_ = {'wikidata': qnum}
            if viaf: ids_['viaf'] = viaf
            if isni: ids_['isni'] = isni
            try:
                add = [] 
                if not e.remote_ids.get('wikidata'):
                    add.append('Wikidata ID')
                if not e.remote_ids.get('isni'):
                    add.append('ISNI')
                if not e.remote_ids.get('viaf'):
                    add.append('VIAF')
                e.remote_ids = {**ids_, **e.remote_ids}
                msg = 'add ' + ','.join(add)
            except AttributeError:
                msg = 'add ids'
                e.remote_ids = ids_
            r = e.save(msg)
            print(olid, msg, e.remote_ids, r)


