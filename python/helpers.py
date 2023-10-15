import datetime

def counter(json, key, value):
    count = 0
    for item in json:
        if item[key] == value:
            count += 1
    return count

def totaler(json, key, value, key_to_total):
    total = 0
    for item in json:
        if item[key] == value:
            total += item[key_to_total]
    return total

def map_counter(json, key):
    map_generated = {}
    for item in json:
        map_generated[item[key]] = map_generated.get(item[key],0) + 1
    return map_generated

def map_totaler(json, map_key, value_key):
    map_generated = {}
    for item in json:
        map_generated[item[map_key]] = map_generated.get(item[map_key],0) + item[value_key]
    return map_generated

def max_map_alphabetically(map):
    keys = list(map.keys())
    keys.sort()
    max_key = keys[0]
    max_value = map[keys[0]]
    for key in keys:
        if map[key] > max_value:
            max_key = key
            max_value = map[key]
    return max_key

def min_map_alphabetically(map):
    keys = list(map.keys())
    keys.sort()
    min_key = keys[0]
    min_value = map[keys[0]]
    for key in keys:
        if map[key] < min_value:
            min_key = key
            min_value = map[key]
    return min_key

def date_to_datetime(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d")

state_to_abbreviation = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}