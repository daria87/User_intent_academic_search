from reading_from_files import get_files, get_root,to_pickle
from processing import get_quer_doc_nb, process_queries
import re


def get_queries_co_2005(files):
    d = {'qid': '', 'query':''}
    l_q = []
    for file in files:
        qid = get_quer_doc_nb(file)
        root = get_root(file)
        for child in root:
            print(child)
            for subchild in child:
                print(subchild)
                if subchild.tag == "title":
                    #print("text",subchild.text)
                    l = [qid,subchild.text]
                    d_q = dict(zip(d, l))
                    l_q.append(d_q)
    return l_q

def get_queries_co_2004(files):
    d = {'qid': '', 'query':''}
    l_q = []
    for file in files:
        qid = get_quer_doc_nb(file)
        root = get_root(file)
        for child in root:
            if child.tag == "title":
                #print("text",subchild.text)
                l = [qid,child.text]
                d_q = dict(zip(d, l))
                l_q.append(d_q)
    return l_q

def get_queries_cas_2004(files):
    d = {'qid': '', 'query':''}
    l_q = []
    l_m_proc = []
    for file in files:
        qid = get_quer_doc_nb(file)
        root = get_root(file)
        for child in root:
            if child.tag == "title":
                text = process_queries(child.text)
                query = " ".join(text.split())
                l = [qid, query]
                d_q = dict(zip(d, l))
                l_q.append(d_q)
    return l_q

def get_queries_cs_2005(files):
    d = {'qid': '', 'query':''}
    l_q = []
    for file in files:
        found = False
        #print(file)
        query =  ""
        l_m_proc = []
        qid = get_quer_doc_nb(file)
        root = get_root(file)
        for child in root:
            for subchild in child:
                if (subchild.tag == "title") and (subchild.text):
                        found = True
                        l = [qid, subchild.text]
                        d_q = dict(zip(d, l))
                        l_q.append(d_q)
                        #print(l_q)
                elif (subchild.tag == "castitle") and (not found):
                        pattern = r"\((.*?)\)"
                        match = re.findall(pattern, subchild.text)
                        l_m = match
                        for el in l_m:
                            el = process_queries(el)
                            l_m_proc.append(el)
                        query = " ".join(l_m_proc)
                        query = " ".join(query.split())
                        l = [qid, query]
                        d_q = dict(zip(d, l))
                        l_q.append(d_q)
    return l_q

#l_files_2005_1 = get_files('../input/CO+S_2005')
#l_files_2005_2 = get_files('../input/CAS_2005')
#l_q_2005_1 = get_queries_co(l_files_2005_1)
#l_q_2005_2 = get_queries_cs(l_files_2005_2)
#l_com = l_q_2005_1 + l_q_2005_2
#print(l_com)
l_files_2004_CAS =  get_files('../input/topics-2004-CAS')
print(len(l_files_2004_CAS))
l_files_2004_CO =  get_files('../input/topics-2004-CO')
print(len(l_files_2004_CO))
l_q_2004_CAS = get_queries_cas_2004(l_files_2004_CAS)
print("l_cas",l_q_2004_CAS)
l_q_2004_CO = get_queries_co_2004(l_files_2004_CO)
print("l_co",l_q_2004_CO)
l_com = l_q_2004_CAS + l_q_2004_CO
print(l_com)
to_pickle(l_com,'../output/queries_2004')

"""
l_articles = get_long_texts(l_se,"bibl")
print(len(l_articles))
for el in l_articles:
    if el["docid"] == "pc/2002/b2042.xml":
        print(el)

s = "notification cues.<ref rid="" type="">13</ref><super>,</super><ref rid="" type="">14</ref> This lets the user"
s = re.sub("\<ref(.*?)\>","",s)
s = re.sub("\<\/ref\>", "", s)
print(s)
"""