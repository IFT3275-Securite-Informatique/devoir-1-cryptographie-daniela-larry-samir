from collections import Counter
from typing import List, Dict, Tuple
import nltk
nltk.download('europarl_raw')
from nltk.corpus import europarl_raw
from crypt import *
from typing import Dict, Tuple
import random as rnd
from tqdm import tqdm
from spellchecker import SpellChecker

def decrypt(C):
  M=""
  
  french_text = europarl_raw.french.raw()

  most_common_caracters, most_common_bicaracters = frequences_analysis_plain_text(french_text)

  most_common_symbols, splitted_cryptogram = frequences_analysis_cryptogram(C)

  K = create_key(most_common_caracters, most_common_bicaracters, most_common_symbols)

  for b in splitted_cryptogram:
    M += K[b]

  return M

def replace_char_with_bichar():
  pass

def frequences_analysis_cryptogram(C: str):
  l = len(C)
  ajusted_cryptogram = C

  if l % 8 != 0:
    ajusted_cryptogram = "0" * (8 - (l % 8)) + C

  splitted_cryptogram = [ajusted_cryptogram[i:i + 8] for i in range(0, l, 8)]

  most_common_strings = get_ordered_dict(Counter(splitted_cryptogram))

  return most_common_strings, splitted_cryptogram

def frequences_analysis_plain_text(text: str) -> Tuple[Dict, Dict]:
  most_common_caracters = get_ordered_dict(Counter(text))
  most_common_bicaracters = get_ordered_dict(Counter(cut_string_into_pairs(text)))
  return most_common_caracters, most_common_bicaracters

def get_ordered_dict(frequences: Counter) -> Dict:
  tuples = frequences.most_common()
  tot = sum(t[1] for t in tuples)
  result = {}
  for s, v in tuples:
    result[s] = (v / tot)*100
  return result

def create_key(most_common_characters: Dict, most_common_bicharacters: Dict, most_common_symbols: Dict) -> Dict:
  K = {}
  full_k = {}
  min_pourcentage = list(most_common_bicharacters.values())[0] + 6
  characters = list(most_common_characters.keys())
  do = True
  i = 0
  while do:
    character_purcentage = most_common_characters[characters[i]]
    if character_purcentage > min_pourcentage:
      full_k[characters[i]] = character_purcentage
      i += 1
    else:
      do = False

  nb_bicharacters = 256 - len(full_k)
  if nb_bicharacters > 0:
    bicharacters = list(most_common_bicharacters.keys())
    bicharacters_percentages = list(most_common_bicharacters.values())
    for i in range(nb_bicharacters):
      full_k[bicharacters[i]] = bicharacters_percentages[i]

  symbols = list(most_common_symbols.keys())
  tmp_keys = list(full_k.keys())
  for i in range(len(symbols)):
    K[symbols[i]] = tmp_keys[i]

  return K
    