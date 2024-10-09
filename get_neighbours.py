import difflib
import requests

from countries_names import countries_polish
from countries_dict import countries_dict

SIMILARITY_THRESHOLD = 0.5

def find_the_country_name_in_polish(name):
    best_score = 0
    best_country = ""
    
    for c in countries_polish:
        similarity = difflib.SequenceMatcher(None, c, name).ratio()
        if c[0] == name[0] and similarity > best_score:
            best_score = similarity
            best_country = c
    
    if best_score > SIMILARITY_THRESHOLD:
        return best_country, best_score
    return None, None
    

def are_strings_almost_equal(str1, str2, threshold):
    similarity = difflib.SequenceMatcher(None, str1, str2).ratio()
    # print(similarity)
    return similarity >= threshold

# Example usage

# threshold = 0.7  # 70% similarity
# print(are_strings_almost_equal(str1, str3, threshold))  # Output: True or False

def get_neighbours(country_code):
    url = "http://api.geonames.org/neighboursJSON"
    params = {
        'country': country_code,
        'username': 'trampek86'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    if 'geonames' in data:
        neighbours = [country['countryName'] for country in data['geonames']]
        return neighbours
    else:
        return "No neighbouring countries found."


mock_names = ["Niemczech", "Włoszech", "latarka", "Wielkiej Brytanii", "Anglii" "pies", "o", "i"]

def english_name_to_neighbours(name):
    url = "http://api.geonames.org/searchJSON"
    if name is not None:
        params = {
            'q': name,
            'featureCode': 'PCLI',  # 'PCLI' indicates country
            'maxRows': 1,
            'username': 'trampek86',  # Replace with your GeoNames username
            'lang': 'en'  # Specify language as Polish
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data['geonames']:
            cc = data['geonames'][0]['countryCode']
            n = get_neighbours(cc)
            # print(name, cc, n)
            return n
        
def select_country_name_from_prompt(prompt):
    best_country = None
    best_score = 0
    for w in prompt.split():
        c, s = find_the_country_name_in_polish(w)
        if s is not None and s > best_score:
            best_score = s
            best_country = c
    if best_country is not None:
        return countries_dict[best_country]
    
def get_all_countries_from_answer(answer):
    cs = []
    for w in answer.split():
        c, s = find_the_country_name_in_polish(w)
        if s is not None and s > SIMILARITY_THRESHOLD:
            cs.append(countries_dict[c])
    return list(set(cs))

def evaluate_answer(country, answer):
    score = 0
    real_neighbours = english_name_to_neighbours(country)
    answer_neighbours = get_all_countries_from_answer(answer)
    # print(real_neighbours, "real")
    # print(countries_from_answer, "answer")
    for c in answer_neighbours:
        if c in real_neighbours:
            score += 1
    return score

def english_to_polish_country_name(name):
    for key, value in countries_dict.items():
        if value == name:
            return key


# def polish_conjugated_name_to_english_country_name(name):
#     cn_polish, _ = find_the_country_name_in_polish(name)
#     if cn_polish is not None:
#         return countries_dict[cn_polish]

# print(polish_prompt_to_neighbouring_countries("W Słowenii mieszka dużo niedźwiedzi."))
# print(polish_prompt_to_neighbouring_countries("Zamieszkałem wraz z przyjaciółmi w Czechach."))

# print(polish_conjugated_name_to_english_country_name("Rosji"))


# c = select_country_name_from_prompt("Aktualnie odbywają się wybory w Tunezji.")
# print(english_name_to_neighbours(c))

# print(get_all_countries_from_answer("Polska graniczy z Niemcami, Czechami i Słowacją"))
# print(evaluate_answer("Polska", "Polska graniczy z Niemcami, Czechami i Słowacją"))


