from reading_from_files import read_xml, read_pickle,to_pickle
from processing import preprocess, parse_doc, make_same_path,remove_excessive_spaces
from lxml import etree

"""
for thorough we need: articles, (article, bdy), abstracts(abs,FM) paragraphs(ip,p (no need to get separately), 
sections(s,ss), lists(list,lc,l1,la), figures(fig), tables(tbl), vitaes(vt), formulas(tf(no need to extract separately)
references (bm, bibl,bb, bib), others (st,ti(no need to extract)
"""


def get_small_element(paper_d):
    """
    :param paper_d: the dictionary where the key is the path to the paper and the value is the text of the paper
    :return: a list of dictionaries for this paper that contains non-concatenated small xml elements.
    Docno is a path of an element in xml tree
    """
    try:
        f_pr = parse_doc(paper_d["text"])
        f_pre = preprocess(f_pr)
        d = {'docid': '', 'docno': '', 'tag': '', 'text':''}
        l_paper_se = []
        root = etree.fromstring(f_pre)
        tree = etree.ElementTree(root)
        for elt in root.iter():
            path = make_same_path(tree.getpath(elt))
            l = [paper_d["docid"],path,elt.tag,elt.text]
            d_paper = dict(zip(d, l))
            l_paper_se.append(d_paper)
    except etree.XMLSyntaxError:
        print(SyntaxError)
    return l_paper_se




def get_list_small_elements(l_papers):
    """
    :param l: a list of dictionaries with all the papers and their path
    :return: a list of all small elements for each paper. Key: path of the paper, value: list of dictionaries
    """
    l_se = []
    for paper in l_papers:
        l_paper_se = get_small_element(paper)
        docid = paper["docid"]
        d = {docid:l_paper_se}
        l_se.append(d)
    return l_se


def get_long_texts(l_se,elname):
    """
    :param l_se: a list of small elements of one paper
    :param elname: the name of the element that we want the text of
    :return: a list of concatenated texts for the elements of each type
    """
    path_s = ""
    s = ""
    l_longel = []
    d = {'docno': '', 'tag': '', 'text': ''}
    beg_section = False
    for d_el in l_se:
        l_spl = d_el['docno'].split("/")
        if (elname in d_el['docno']):
            if (l_spl[-1].startswith(elname)): # if the element is at the end of the path
                if not beg_section:
                    beg_section = True # beginning of the section
                    path_s = d_el['docno']
                else:
                    l = [path_s,elname,remove_excessive_spaces(s).lstrip(" ")] #getting all the text
                    d_fin = dict(zip(d, l))
                    if d_fin['text']:
                        l_longel.append(d_fin)
                        path_s = d_el['docno']
                        s = ""
            else:
                if d_el["text"]:
                    s = s + " "+ d_el["text"]
    l = [path_s, elname, remove_excessive_spaces(s).lstrip(" ")] #if it is the last element
    d_fin = dict(zip(d, l))
    if d_fin["text"]:
        l_longel.append(d_fin)
    return l_longel

def get_list_long_text(l_se,el_name):
    """
    :param l_se: a list of small elements for all papers
    :param el_name: the name of the element (eg: sec, abs)
    :return: list of dictionaries with full texts of the elements: key: path of the paper, value: list of dictionaries
    """
    l_d_papers = []
    for d_paper in l_se:
        for path in d_paper.keys():
            d = {}
            l_longel = get_long_texts(d_paper[path],el_name)
            if l_longel:
                d[path] = l_longel
                l_d_papers.append(d)
    return l_d_papers

def get_key_and_flatten(l_d_papers):
    """
    flattens the list of dictionaries with lists as values to a list of dictionaries with strings as values
    :param l_d_papers: list of dictionaries for all the papers: key: paper, value: all the elements
    :return:
    """
    l_flat = []
    for d_paper in l_d_papers:
        for path, l_d_el in d_paper.items():
            for d_el in l_d_el:
                path = path.rstrip(".xml")
                d_el['docid'] = path
                l_flat.append(d_el)
    return l_flat




l = read_pickle('../output/inex-1.4')


l_se = get_list_small_elements(l)
print("Len se",len(l_se))
#print(l_se)
l_se_fl = get_key_and_flatten(l_se)
#print(l_se_fl)
l_se_fin = [item for item in l_se_fl if item['text'] is not None]
to_pickle(l_se_fin,'../output/thorough_short_e_2004_corr')
print("Small elements excl nones:",len(l_se_fin))


#2. Getting different elements that we need the texts for

l_art = get_list_long_text(l_se,'article')
l_abs = get_list_long_text(l_se,'abs')
l_body = get_list_long_text(l_se,'bdy')
l_fm = get_list_long_text(l_se,'fm')
l_sec = get_list_long_text(l_se,'sec')
l_ss1 = get_list_long_text(l_se,'ss1')
l_ss2 = get_list_long_text(l_se,'ss2')
l_list = get_list_long_text(l_se,'list')
l_lc = get_list_long_text(l_se,'lc')
l_li = get_list_long_text(l_se,'li')
l_l1 = get_list_long_text(l_se,'l1')
l_la = get_list_long_text(l_se,'la')
l_fig = get_list_long_text(l_se,'fig')
l_fgc = get_list_long_text(l_se,'fgc')
l_tbl = get_list_long_text(l_se,'tbl')
l_vt = get_list_long_text(l_se,'vt')
l_bm = get_list_long_text(l_se,'bm')
l_bibl = get_list_long_text(l_se,'bibl')
l_bb = get_list_long_text(l_se,'bb')
l_bib = get_list_long_text(l_se,'bib')
l_au = get_list_long_text(l_se,'au')
l_app = get_list_long_text(l_se,'app')
l_it = get_list_long_text(l_se,"item")
l_fgb = get_list_long_text(l_se,"fgb")
l_theorem = get_list_long_text(l_se,"theorem")
l_pdt = get_list_long_text(l_se,"pdt")
l_tf = get_list_long_text(l_se,"tf")
l_ie = get_list_long_text(l_se,"index-entry")

#list with long texts
list_comm = l_art+l_body+l_abs+l_fm+l_sec+l_ss1+l_ss2+l_list+l_li+l_lc+l_l1+l_la+l_fig+l_fgc+l_tbl+l_vt+l_bm+l_bibl+l_bb+l_bib+l_au+l_app+l_it+l_fgb+l_pdt+l_theorem+l_tf+l_ie
flatten_comm = get_key_and_flatten(list_comm)
flatten_comm_fin = [item for item in flatten_comm if item['text'] is not None]
print("fl_comm",len(flatten_comm_fin))

to_pickle(flatten_comm_fin,'../output/thorough_long_e_2004_corr')


#focused short ele
#short elements: abs, fm, list,lc,li,l1,la,fig,fgc,tbl,item,theorem
"""
l_abs = get_list_long_text(l_se,'abs')
l_fm = get_list_long_text(l_se,'fm')
l_list = get_list_long_text(l_se,'list')
l_lc = get_list_long_text(l_se,'lc')
l_li = get_list_long_text(l_se,'li')
l_l1 = get_list_long_text(l_se,'l1')
l_la = get_list_long_text(l_se,'la')
l_fig = get_list_long_text(l_se,'fig')
l_fgc = get_list_long_text(l_se,'fgc')
l_tbl = get_list_long_text(l_se,'tbl')
l_it = get_list_long_text(l_se,"item")
l_fgb = get_list_long_text(l_se,"fgb")
l_theorem = get_list_long_text(l_se,"theorem")
l_fgb = get_list_long_text(l_se,"fgb")

l_se_all = l_abs+l_list+l_lc+l_li+l_l1+l_la+l_fig+l_fgc+l_tbl+l_it+l_fgb+l_theorem+l_fgb

flatten_se = get_key_and_flatten(l_se_all)
l_se_fin = [item for item in flatten_se if item['text'] is not None]
l_se_final = add_paper_id(l_se_fin)
print("l_se_fin",l_se_final[0])
print("l_se_fin length:",len(l_se_final))
to_pickle(l_se_final,'../output/focused_short_e_2005')

#getting references

l_bibl = get_list_long_text(l_se,'bibl')
l_bm = get_list_long_text(l_se,'atl')
l_bb = get_list_long_text(l_se,'bb')
l_bib = get_list_long_text(l_se,'bib')
l_au = get_list_long_text(l_se,'au')
l_vt = get_list_long_text(l_se,'vt')
l_ie = get_list_long_text(l_se,"index-entry")
l_ref_el_all = l_bibl+l_bm+l_bb+l_bib+l_au+l_vt+l_ie
flatten_ref = get_key_and_flatten(l_ref_el_all)
flatten_ref_f = add_paper_id(flatten_ref)
flatten_sm_fin = [item for item in flatten_ref_f if item['text'] is not None]
#to_pickle(flatten_sm_fin,'../output/references_2005')

"""






