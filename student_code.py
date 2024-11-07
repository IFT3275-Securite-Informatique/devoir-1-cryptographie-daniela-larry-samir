from collections import Counter
from typing import List, Dict, Tuple
import nltk
nltk.download('europarl_raw')
from nltk.corpus import europarl_raw
from encrypt import *

def decrypt(C):
  M=""
  
  french_text = europarl_raw.french.raw()

  most_common_caracters, most_common_bicaracters = frequences_analysis_plain_text(french_text)

  most_common_symbols, splitted_cryptogram = frequences_analysis_cryptogram(C)

  K = create_key(most_common_caracters, most_common_bicaracters, most_common_symbols)

  for b in splitted_cryptogram:
    M += K[b]

  return M

# def replace_char_with_bichar():
#   pass

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
    

def main():
  C = '01000000000010000000111000110001100011100101111011110101110110100101011001100001000010100100000001110010010111101111010111011010000010000000111000110001010011101111100101100011011110110011000111000101111101100010011000001110001100010010000011001110011000010111000100001010010000001011011011110110110011100110000100110001110001010100011000001110001100010100111011111001011000110111101110111001010100110000011000101101011100001001010010000110'
  M = "es, les nations sur les nations, les vérités sur les erreurs, les erreurs sur les vérités. Tout se "
  R = decrypt(C)
  print(R)
  print(len(R))

if __name__ == '__main__':
  main()