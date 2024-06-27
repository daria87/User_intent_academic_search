from reading_from_files import to_pickle
import xml.etree.ElementTree as ET
from reading_from_files import get_files, get_root
from processing import get_quer_doc_nb
from string import digits
from collections import Counter



def gen_quantisation_2004(exhaustiveness, specificity):
    rel_s = 0
    if exhaustiveness == 3 and specificity == 3:
        rel_s = 1
    elif (exhaustiveness == 2 and specificity == 3) or (exhaustiveness == 3 and specificity == 2) or (exhaustiveness == 3 and specificity == 1):
        rel_s = 0.75
    elif (exhaustiveness == 1 and specificity == 3) or (exhaustiveness == 2 and specificity == 2) or (exhaustiveness == 2 and specificity == 1):
        rel_s = 0.5
    elif (exhaustiveness == 1 and specificity == 2) or (exhaustiveness == 1 and specificity == 1):
        rel_s = 0.25
    return rel_s

def sog_quantisation_2004(exhaustiveness, specificity):
    rel_s = 0
    if exhaustiveness == 3 and specificity == 3:
        rel_s = 1
    elif exhaustiveness == 2 and specificity == 3:
        rel_s = 0.9
    elif (exhaustiveness == 1 and specificity == 3) or (exhaustiveness == 3 and specificity == 2):
        rel_s = 0.75
    elif exhaustiveness == 2 and specificity == 2:
        rel_s = 0.5
    elif (exhaustiveness == 1 and specificity == 2) or (exhaustiveness == 3 and specificity == 1):
        rel_s = 0.25
    elif (exhaustiveness == 2 and specificity == 1) or (exhaustiveness == 1 and specificity == 1):
        rel_s = 0.1
    return rel_s

def get_rel_scores_2004(rel_files):
    l_rel = []
    d = {'docid': '', 'qid':'', 'docno': '', 'tag': '','exhaustivity': '', 'specificity':'','gen_q':0,'sog_q':0,'strict_q':0}
    for file in rel_files:
        try:
            root = get_root(file)
            for child in root:
                if child.tag == "file":
                    filename = child.attrib["file"]
                for subchild in child:
                    if subchild.tag == "path":
                        if subchild.attrib["exhaustiveness"] !="0":
                            qid = get_quer_doc_nb(file)
                            l_t = subchild.attrib["path"].split("/")
                            tag = l_t[-1].rstrip("[" + digits + "]")
                            gen_q = gen_quantisation_2004(int(subchild.attrib["exhaustiveness"]),int(subchild.attrib["specificity"]))
                            sog_q = sog_quantisation_2004(int(subchild.attrib["exhaustiveness"]),int(subchild.attrib["specificity"]))
                            if gen_q == 1:
                                strict_q = 1
                            else:
                                strict_q = 0
                            l = [filename,qid,filename+subchild.attrib['path'],tag,subchild.attrib["exhaustiveness"],subchild.attrib["specificity"],gen_q,sog_q,strict_q]
                            d_rel = dict(zip(d, l))
                            l_rel.append(d_rel)
        except ET.ParseError as e:
            print(f"Error parsing XML file {file}: {e}")
    return l_rel

def get_rel_scores_2005(rel_files):
    l_rel = []
    d = {'docid': '', 'qid':'', 'docno': '', 'tag': '','exhaustivity': '', 'specificity':'','gen_q':0,'strict_q':0}
    for file in rel_files:
        try:
            root = get_root(file)
            for child in root:
                if child.tag == "file":
                    filename = child.attrib["name"]
                for subchild in child:
                    if subchild.tag == "element":
                        if subchild.attrib["exhaustivity"] !="?":
                            qid = get_quer_doc_nb(file)
                            l_t = subchild.attrib["path"].split("/")
                            tag = l_t[-1].rstrip("["+digits+"]")
                            spec_score = round(int(subchild.attrib["rsize"]) / int(subchild.attrib["size"]), 2)
                            gen_q = spec_score * int(subchild.attrib["exhaustivity"])
                            if gen_q == 2.0:
                                strict_q = 1
                            else:
                                strict_q = 0
                            l = [filename,qid,filename+subchild.attrib['path'],tag,subchild.attrib["exhaustivity"],spec_score,gen_q,strict_q]
                            d_rel = dict(zip(d, l))
                            l_rel.append(d_rel)
        except ET.ParseError as e:
            print(f"Error parsing XML file {file}: {e}")
    return l_rel


f = get_files('../input/CO+S_2005_uot')
f2 = get_files('../input/CAS_2005_uot')
#f3 = get_files('../input/assessments-inex04-official')
l_rel1 = get_rel_scores_2005(f)
print(l_rel1)
l_rel2 = get_rel_scores_2005(f2)
l_com = l_rel1+l_rel2
print(l_com)
#l_2004 = get_rel_scores_2004(f3)
#print(l_2004)
#print(len(l_2004))
#to_pickle(l_2004,'../output/relevance_scores_2004')
to_pickle(l_com,'../output/relevance_scores_2005_uot')


"""
tags = [d['tag'] for d in l_com]

# Counting occurrences of each color
tag_counts = Counter(tags)

# Printing the count of each color
for tag, count in tag_counts.most_common():
    print(f"{tag}: {count}")


"""
