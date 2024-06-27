import string
import re

def get_quer_doc_nb(file):
    l_q = file.split("/")
    qid = l_q[-1].rstrip(".xml")
    return qid

def process_queries(query):
    query = query.replace("//p","")
    query = query.replace("//article", "")
    query = query.replace("//abs", "")
    query = query.replace("//sec", "")
    query = query.replace("//bdy", "")
    query = query.replace("//fm", "")
    query = query.replace("//atl", "")
    query = query.replace("//au", "")
    query = query.replace("//abs", "")
    query = query.replace("//kwd", "")
    query = query.replace("//tig", "")
    query = query.replace("//st", "")
    query = query.replace("//ip1", "")
    query = query.replace("//bb", "")
    query = query.replace("//bib", "")
    query = query.replace("//atl", "")
    query = query.replace("//bm", "")
    query = query.replace("//vt", "")
    query = query.replace("//yr", "")
    query = query.replace("//fig", "")
    query = query.replace("//fgc", "")
    query = query.replace("//snm", "")
    query = query.replace("about", "")
    query = query.replace("(abs|kwd)", "")
    query = query.replace("(p| fgc)", "")
    query = re.sub(r'\b(OR|AND)\b', '', query, flags=re.IGNORECASE)
    translation_table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    query = query.translate(translation_table)
    query = re.sub(r'\s+', ' ', query).strip()
    return query

def parse_doc(doc):
    """
    :param file: xml doc from inex collection
    :return: doc stripped of all the characters that are not parseable
    """
    doc = doc.replace('&ndash;', '–')
    doc = doc.replace('&mdash;', '—')
    doc = doc.replace('&copy;', 'copyright')
    doc = doc.replace('&ldquo;','"')
    doc = doc.replace('&rdquo;','"')
    doc = doc.replace('&rsquo;',"'")
    doc = doc.replace('&lsquo;',"'")
    #doc = doc.replace('\n', "")
    doc = re.sub('\&[a-zA-Z]+\;', ' ', doc)
    return doc


def preprocess(f):
    f = re.sub("\<ref(.*?)\>","",f)
    f = re.sub("\<\/ref\>", "", f)
    f = re.sub("\<super\>", "", f)
    f = re.sub("\<\/super\>", "", f)
    f = re.sub("\<it\>", "", f)
    f = re.sub("\<\/it\>", "", f)
    f = re.sub("\<b\>", "", f)
    f = re.sub("\<\/b\>", "", f)
    f = re.sub("\<tt\>", "", f)
    f = re.sub("\<\/tt\>", "", f)
    f = re.sub("\<scp\>", "", f)
    f = re.sub("\<\/scp\>", "", f)
    f = re.sub("\<tmath\>", "", f)
    f = re.sub("\<\/tmath\>", "", f)
    #f = re.sub("\<list(.*?)\>(.*?)\<\/list\>", "", f, flags= re.DOTALL)
    #f = re.sub("\<\/item\>\<item\>\<label\> \<\/label\>", "ELE", f, flags=re.DOTALL)
    return f

def make_same_path(path):
    """
    makes the path the sane
    :return: the path that is the same as in relevance scores
    """
    l_corr = []
    l = path.split("/")
    for el in l:
        if "]" in el:
            l_corr.append(el)
        else:
            el = el+"[1]"
            l_corr.append(el)
    return "/".join(l_corr).lstrip("[1]")

def remove_excessive_spaces(text):
    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', text).strip()
    return cleaned_text

