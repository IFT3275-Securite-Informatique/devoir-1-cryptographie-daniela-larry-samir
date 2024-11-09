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

# Initialiser le vérificateur d'orthographe français
spell = SpellChecker(language='fr')

def decrypt(C):
  M=""
  french_text = europarl_raw.french.raw()
  most_common_caracters, most_common_bicaracters = frequences_analysis_plain_text(french_text)
  symbols = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i',
             ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U',
             'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a',
             'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û',
             '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd',
             'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e',
             'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne',
             'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa',
             'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss',
             'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om',
             ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u',
             "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn',
             'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
  _, best_key = hill_climbing(C, most_common_caracters, most_common_bicaracters, symbols, 100000)
  M = decrypt_C(C, best_key)
  return M

def hill_climbing(C, character_freqs, bicharacter_freqs, symbols, iterations=1000000):
  all_bytes = [format(i, '08b') for i in range(256)]
  alphabet = symbols[:len(all_bytes)]
  initial_mapping = rnd.sample(alphabet, len(alphabet))
  best_key = dict(zip(all_bytes, initial_mapping))

  best_key_score = score_text(decrypt_C(C, best_key), character_freqs, bicharacter_freqs)

  for _ in tqdm(range(iterations), desc="Hill Climbing"):
    new_key = change_key(best_key.copy())  # Ensure new_key is a copy
    decrypted_text = decrypt_C(C, new_key)
    new_key_score = score_text(decrypted_text, character_freqs, bicharacter_freqs)

    if new_key_score > best_key_score:
        best_key_score = new_key_score
        best_key = new_key

  return best_key_score, best_key

def decrypt_C(bits, key):
  decrypted_text = []
  for i in range(0, len(bits), 8): 
    byte = bits[i:i+8]
    decrypted_text.append(key.get(byte, '?'))
  return ''.join(decrypted_text)

def penalize_rare_sequences(text):
  RARE_SEQUENCES = {'aa': -5, 'ii': -5, 'uu': -5, 'lk': -5, 'ph': -5, 'zx': -5, 'pq': -5, 'jz': -5, 
  'mz': -5, 'xk': -5, 'sx': -5, 'cq': -5, 'dz': -10, 'fz': -10, 'vx': -10}
  penalty = 0
  for seq, score in RARE_SEQUENCES.items():
    penalty += text.count(seq) * score
  return penalty

def score_text(text, letter_freqs, digram_freqs):
  score = 0
  words = text.split(" ")
  num_of_french_words = 0
  for word in words:
      if is_french_word(word):
          num_of_french_words += 1
          score += 10
          for letter in word:
              if letter in letter_freqs:
                  score += 1
          for digram in [word[i:i+2] for i in range(len(word) - 1)]:
              if digram in digram_freqs:
                  score += 1
  if num_of_french_words == len(words):
      score += 100

  score -= penalize_rare_sequences(text)

  if len(text) < 8 and len(text) > 3:
      score =+ 10
  else:
      score -= 10

  return score

def is_french_word(word):
  return word in spell

def change_key(key):
  items = list(key.items())
  i, j = rnd.sample(range(len(items)), 2)
  byte_i, byte_j = format(i, '08b'), format(j, '08b')
  key[byte_i], key[byte_j] = key[byte_j], key[byte_i]
  return key

def frequences_analysis_plain_text(text: str) -> Tuple[Dict, Dict]:
  most_common_caracters = get_ordered_dict(Counter(text))
  most_common_bicaracters = get_ordered_dict(Counter([text[i:i+2] for i in range(len(text) - 1)]))
  return most_common_caracters, most_common_bicaracters

def get_ordered_dict(frequences: Counter) -> Dict:
  tuples = frequences.most_common()
  tot = sum(t[1] for t in tuples)
  result = {s: v / tot for s, v in tuples}
  return result

