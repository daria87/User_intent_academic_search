# U of tampere
import xml.etree.ElementTree as ET
from processing import parse_doc
from reading_from_files import read_xml, get_root_s,to_pickle
d = {'docno': '', 'qid':'', 'rank': ''}

"""
root = get_root_s('../input/0.xml')
count = 0
for child in root:
    print(child.attrib)
    for subchild in child:
        print(subchild.attrib)
        if subchild.tag == "result":
            pass
"""
def get_run_results(run):
    l_run = []
    tree = ET.parse(run)
    root = tree.getroot()
    d = {"qid":"","docno":""}
    # Print the attributes of the root element
    # Iterate over topics and results
    for topic in root.findall('topic'):
        topic_id = topic.attrib['topic-id']
        qid = topic_id
        print(f"\nTopic ID: {topic_id}")
        for result in topic.findall('result'):
            file = result.find('file').text
            path = result.find('path').text
            docno = file+path
            print(docno)
            #rank = result.find('rank').text
            rsv = result.find('rsv').text
            l = [qid,docno]
            d_run = dict(zip(d, l))
            l_run.append(d_run)
    return l_run

l_run = get_run_results('../input/ut_co_overlap.xml')
print(len(l_run))
to_pickle(l_run,"../output/ut_co_overlap")



