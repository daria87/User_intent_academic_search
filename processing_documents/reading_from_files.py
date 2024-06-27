import glob
import pickle
import os
from processing import parse_doc
import xml.etree.ElementTree as ET

#onlyfiles = [f for f in listdir("../input/inex-1.6") if isfile(join("../input/inex-1.6", f))]
#print(onlyfiles)

def read_xml(path):
    # Open the XML file and read its contents into a string
    with open(path, 'r', encoding='utf-8') as file:
        xml_string = file.read()
    return xml_string

def parsed_path(path):
    l = path.split("/")
    return "/".join(l[-3:])

def contains_digits(s):
    return any(char.isdigit() for char in s)

def read_all_doc(path):
    l_d = []
    l_filenames = []
    count=0
    count_f = 0
    d = {'docid': '', 'text': 0}
    for filename in glob.iglob(path + '**/**', recursive=True):
        count_f +=1
        try:
            if (".xml" in filename) and ("volume" not in filename):
                if filename not in l_filenames:
                    l = [parsed_path(filename),read_xml(filename)]
                    d_f = dict(zip(d, l))
                    l_d.append(d_f)
                    l_filenames.append(filename)
        except UnicodeError:
            print("Unicode Error")
    return l_d

def to_pickle(l,filename):
    try:
        geeky_file = open(filename, 'wb')
        pickle.dump(l, geeky_file)
        geeky_file.close()
    except:
        print("Something went wrong")

def read_pickle(file):
    f = open(file, 'rb')
    l_d = pickle.load(f)
    return l_d

def get_files(folder_path):
    l = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if "xml" in filepath:
            l.append(filepath)
    return sorted(l)

def get_root(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

def get_root_s(filename):
    s = read_xml(filename)
    prepr = parse_doc(s)
    root = ET.fromstring(prepr)
    return root



l = read_all_doc('../input/inex-1.4')
print(len(l))
to_pickle(l,'../output/inex-1.4')
#l2 = read_all_doc('../input/inex-1.4')
#to_pickle(l2,'../output/inex-1.4-full')
#l_d = read_pickle('../output/inex-1.6-full')
#print(l_d)
