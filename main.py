import csv
import requests
import json
import codecs
import datetime
from operator import itemgetter


def get_entity_label(entity, id):
    return entity['entities'][id]["labels"]["en"]


def get_actors(movie, id):
    actors = list()
    for actor in movie['entities'][id]["claims"]["P161"]:
        actors.append(actor["mainsnak"]["datavalue"]["value"]["id"])
    return actors


def get_actor_gender(actor, actor_id):
    if "P21" in actor['entities'][actor_id]["claims"]:
        return actor['entities'][actor_id]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"]
    else:
        return None


def select_result(results):
    if results['search-continue'] > 1:
        count = 1
        for result in results['search']:
            if "label" in result:
                label = result['label']
            else:
                label = ""

            if "description" in result:
                description = result['description']
            else:
                description = ""

            print("Result n°"+str(count)+' :')
            print(label + " -> " + description)
            count = count + 1

        selection = input('Please type your choice number: ')
        return results['search'][int(selection)-1]

    else:
        return results['search'][0]


def get_entities(string):
    url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&language=fr&format=json&search="+string
    response = requests.get(url)
    content = json.loads(codecs.decode(response.content, 'utf-8'))

    # print(url)
    # print("> Get Entity: " + str(content))
    return content


def get_entity(id):
    url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids="+id
    response = requests.get(url)
    content = json.loads(codecs.decode(response.content, 'utf-8'))

    # print(url)
    # print("> Get Entity: " + str(content))
    return content


movie = input('Please type your movie: ')
result_movie = get_entities(movie)

if result_movie['search-continue'] == 0:
    print("There is no result for your request")
else:
    movie_selected = select_result(result_movie)
    movie = get_entity(movie_selected['id'])
    actors = get_actors(movie, movie_selected['id'])
    print(actors)

    genders = dict()

    for actor_id in actors:
        actor = get_entity(actor_id)
        gender = get_actor_gender(actor, actor_id)

        if gender in genders:
            genders[gender] = genders[gender]+1
        else:
            genders[gender] = 1

        print(str(get_entity_label(actor, actor_id)["value"]) + " => " + str(gender))

    print(genders)