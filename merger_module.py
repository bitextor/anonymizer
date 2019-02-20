#!/usr/bin/env python

# merge-module: Merges the entities extracted by the other modules, avoiding duplicates. 

import logging
import entity


"""
Solves overlapping between entities in the same sentence
  sentence: Sentence containing the entities
  entities: List of entities 
The list of entities is sorted by position and checked from the beginning.
If two consecutive entities overlap (fully or partially), it is, 
the beginning of the second one is between the beginning and the end of the first one,
both entities are merged into a single entity, containing the union of both entities.
 
"""
def mono_merge(sentence, entities):  
  length = len(entities)  
  if length==0 or length==1:
    return entities
  index = 0
  entities = entity.sort_by_position(entities)
  while index < len(entities):  
    current_ent = entities[index]
    #last item
    if index == len(entities)-1:
      return entities
    else:   
      next_ent = entities[index+1]
      cur_end = current_ent.start + current_ent.length
      next_end = next_ent.start + next_ent.length
      #Overlapping:
      if (current_ent.start <= next_ent.start) and (cur_end >= next_ent.start):
        #print("*************** OVERLAPPING ***************")
        #print("ENTITIES: " + entity.serializeArray(entities))
        #print("CURRENT: " + current_ent.serializeEntity())
        #print("NEXT: " + next_ent.serializeEntity())
  
        new_start = current_ent.start  #because entities are sorted 
        new_end = max(cur_end, next_end)
        new_length = new_end - new_start
        if current_ent.length >= next_ent.length:
          new_type = current_ent.type
        else:
          new_type = next_ent.type  
        new_entity = entity.Entity(current_ent.start, new_length, new_type, sentence[new_start:new_end])
        del entities[index+1]
        del entities[index]        
        entities.append(new_entity)
        #print("MERGED: " + new_entity.serializeEntity())
        entities = entity.sort_by_position(entities)
        index = 0
      else:
        index += 1  

"""
Solves tagging  of named entities when only in one side of the parallel sentence.
  src_sentence: Source sentence
  src_entities: List of entities found in the source sentence
  trg_sentence: Target sentence
  trg_entities: List of entities found in the target sentence
  
  
"""
def para_merge(src_sentence, src_entities, trg_sentence, trg_entities):
  """
  New approach on merging NER entities:

  * Entity text is in A and B:
    * Keep the label as in A
  * Entity text is in A and not in B:
    * Entity has no uppercased words (excluding string beginning): Ignore in both
      * example: "My cousin's friend is ugly" {} - "El amigo de mi primo es feo" {El amigo de mi primo: PER}
      * becomes: "My cousin's friend is ugly" {} - "El amigo de mi primo es feo" {}
    * Entity text has an uppercased part, the part in uppercase is not in any entity in B, and the uppercased part can be found also in B : Tag the entity in both
      * example: "Tesla's Model S is expensive" {Tesla's Model S: MISC} - "El Model S de Tesla es caro" {Tesla: ORG}
      * becomes: "Tesla's Model S is expensive" {Tesla's Model S: MISC} - "El Model S de Tesla es caro" {Model S: MISC, Tesla: ORG}
    * Entity text is not present in B: Keep the entity in A, it's unsafe to remove 
       * example: "Tesla's Model S is expensive" {Tesla's Model S: MISC} - "El Modelo S de Tesla es caro" {Tesla: ORG}
       * remains the same.
  """
  return src_entities, trg_entities   
    
"""
Merges entities extracted from a parallel sentence
  src: Source
  trg: Target
  src_regex: Entites extracted by the regex_module in the source
  src_addresses: Entities extracted by the address_module in the source
  src_names: Entities extracted by the names_module in the source
  trg_regex: Entities extracted by the regex_module in the target
  trg_address: Entities extracted by the address_module in the target
  trg_names: Entities extracted by the names_module in the target
"""
def merge(src, trg, src_regex, src_addresses, src_names, trg_regex, trg_addresses, trg_names): 

  results = dict()
  

  src_entities = [] 
  trg_entities = [] 
  
  
  src_entities.extend(src_regex)
  src_entities.extend(src_addresses)
  src_entities.extend(src_names)
  
    
  trg_entities.extend(trg_regex)
  trg_entities.extend(trg_addresses)
  trg_entities.extend(trg_names)
  
 
  src_merged, trg_merged = para_merge(src, src_entities, trg, trg_entities)
      
  l1 = mono_merge(src, src_merged)
  l2 = mono_merge(trg, trg_merged)
  

  results["l1"] = l1
  results["l2"] = l2
  
  
 
  return results



 


 


