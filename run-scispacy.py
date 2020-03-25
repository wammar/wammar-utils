# run scispacy's largest model to link entities of interest.

import scispacy
import spacy

from scispacy.abbreviation import AbbreviationDetector
from scispacy.umls_linking import UmlsEntityLinker
from scispacy.umls_semantic_type_tree import SemanticTypeNode

from typing import List, Set, Dict, Tuple, Optional

# load large model.
nlp = spacy.load("en_core_sci_lg")
# add abbreviation pipe to the model.
abbreviation_pipe = AbbreviationDetector(nlp)
nlp.add_pipe(abbreviation_pipe)
# add UMLS linker to the model.
linker = UmlsEntityLinker(resolve_abbreviations=True)
nlp.add_pipe(linker)

text = """
Myeloid derived suppressor cells (MDSC) are immature
myeloid cells with immunosuppressive activity.
They accumulate in tumor-bearing mice and humans
with different types of cancer, including hepatocellular
carcinoma (HCC).
"""
doc = nlp(text)

# process sentences.
# print('sents:')
# print(list(doc.sents))

# process abbreviations.
# print('abbreviations:')
# for abrv in doc._.abbreviations:
#   print(f"{abrv} \t ({abrv.start}, {abrv.end}) {abrv._.long_form}")

# find all ancestors of a semantic type.
def get_semantic_type_lineage(partial_list: List[SemanticTypeNode]):
  current_node = partial_list[-1]
  if current_node.level <= 1:
    # no more ancestors to trace.
    return partial_list
  parent_node = linker.umls.semantic_type_tree.get_parent(current_node)
  partial_list.append(parent_node)
  return get_semantic_type_lineage(partial_list)

# TODO(wammar): curate the list of relevant types.
ST21PV_TYPES = [
    'T005',
    'T007',
    'T017',
    'T022',
    'T031',
    'T033',
    'T037',
    'T038',
    'T058',
    'T062',
    'T074',
    'T082',
    'T091',
    'T092',
    'T097',
    'T098',
    'T103',
    'T168',
    'T170',
    'T201',
    'T204']
# check if a semantic type ID corresponds to a grandchild of a list of "great fathers".
# By default, the set of great fathers include the 21 types used in the MedMentions st21pv subset.
def is_subtype_relevant(subtype_id: str, relevant_type_ids: List[str]=ST21PV_TYPES):
  child_type_node = linker.umls.semantic_type_tree.get_node_from_id(subtype_id)
  lineage_nodes = get_semantic_type_lineage([child_type_node])
  lineage_ids = [node.type_id for node in lineage_nodes]
  overlap = set(lineage_ids).intersect(set(relevant_type_ids))
  return len(overlap) > 0

# process entity mentions.
for mention in doc.ents:
  # process each linked entity, higher scoring links appear earlier.
  for cui, score in ent._.umls_ents:
    # ignore linked entities with score < threshold.
    THRESHOLD = 0.85
    if score < THRESHOLD:
      break
    umls_entity = linker.umls.cui_to_entity[cui]
    # only use this entity if one of its types is relevant.
    relevant_types = []
    for subtype_id in umls_entity.types:
      if is_subtype_relevant(subtype_id = subtype_id):
        relevant_types.append(subtype_id)
    if not relevant_types:
      continue
    # go to the next mention as soon as you find one relevant entity which meets the threshold.
    print(f"entity: {mention}, relevant types: {relevant_types}")
    continue
import pdb; pdb.set_trace()
