from reading_from_files import read_xml, read_pickle,to_pickle

l_rel = read_pickle("../output/relevance_scores_2005")
#print(l_rel)
l_rel_p = []
for el in l_rel:
    l_rel_p.append(el["docno"])
print("Len relevance",len(l_rel_p))

l_thorough_sm = read_pickle("../output/thorough_short_e_2005")
l_thorough_lar = read_pickle("../output/thorough_long_e_2005")
l_thorough = l_thorough_sm+l_thorough_lar
l_thorough_fin = []
l_thorough_p = []
for el_t in l_thorough:
    l_thorough_p.append(el_t['docno'])
print("len thorough",len(l_thorough_p))


set1 = set(l_rel_p)
set2 = set(l_thorough_p)

# Find the intersection of two sets
common_elements = set1.intersection(set2)

# Convert the set back to a list
common_elements_list = list(common_elements)
print("common len",len(common_elements_list))
#print(common_elements_list)
l_excluded = [x for x in l_rel_p if x not in common_elements]
#print("elements excluded", l_excluded)
print("len elements excluded", len(l_excluded))
print("Elements excluded:",l_excluded)
