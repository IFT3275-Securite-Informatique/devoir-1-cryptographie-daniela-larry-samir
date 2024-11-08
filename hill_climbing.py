from collections import Counter
from typing import List, Dict, Tuple
import random as rnd
from tqdm import tqdm
from spellchecker import SpellChecker
import nltk
nltk.download('europarl_raw')
from nltk.corpus import europarl_raw

# Initialiser le vérificateur d'orthographe français
spell = SpellChecker(language='fr')

def hill_climbing(C, character_freqs, bicharacter_freqs, symbols, iterations=1000):
    all_bytes = [format(i, '08b') for i in range(256)]
    alphabet = symbols[:len(all_bytes)]
    initial_mapping = rnd.sample(alphabet, len(alphabet))
    best_key = dict(zip(all_bytes, initial_mapping))

    best_key_score = score_text(decrypt(C, best_key), character_freqs, bicharacter_freqs)

    for _ in tqdm(range(iterations), desc="Hill Climbing"):
        new_key = change_key(best_key.copy())  # Ensure new_key is a copy
        decrypted_text = decrypt(C, new_key)
        new_key_score = score_text(decrypted_text, character_freqs, bicharacter_freqs)

        if new_key_score > best_key_score:
            best_key_score = new_key_score
            best_key = new_key

    return best_key_score, best_key

def decrypt(bits, key):
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

if __name__ == '__main__':
    french_text = europarl_raw.french.raw()
    most_common_caracters, most_common_bicaracters = frequences_analysis_plain_text(french_text)

    C = ("01000000000010000000111000110001101010000101111011110101110110100101011001100001000010100100000001110010010111101111010111011010000010000000111000110001101000110101101001100011011110110011000111000101100011100010011000001110001100010010000011001110011000010111000100001010010000001011011010001110110011100110000100110001110001010100011000001110001100011010001101011010011000110111101100010001010100110011001000101101011100001001010011001010")

    symbols = ['ù', '—', '8', '?', 'É', '[', 'è', 'Ê', 'ô', '»', ' ', 'J', 'f', 'j', 'q', '…', 'm', 'S', 'n', 'Î', 'i', 'à', 'L', 'u', 'e', 'B', ';', 'D', 'Q', 'N', 'z', '_', 'ï', '\ufeff', '#', ':', '5', 'k', 'È', ')', 'g', 'é', '7', 'P', '“', '$', '‘', 'l', 'A', ',', "'", 'b', 'ç', 'Â', 'G', '/', '”', 's', 'v', 'I', '!', '0', 'p', 't', 'E', '%', '™', 'À', 'U', 'c', 'â', 'T', 'K', 'ë', '\n', 'y', 'o', 'w', 'M', 'Ç', 'H', '°', 'F', 'î', 'Y', 'ê', '*', 'r', 'x', '-', 'º', '2', '\r', '1', 'R', '.', 'û', 'd', 'V', 'C', '4', 'h', '9', 'a', '6', ']', '•', '«', 'X', '’', '3', 'W', 'O', '(', 'Z', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
    best_key_score, best_key = hill_climbing(C, most_common_caracters, most_common_bicaracters, symbols, 100000)
    R = decrypt(C, best_key)
    print("Texte décrypté:", R)
