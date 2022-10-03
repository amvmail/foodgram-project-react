import json

file_name = 'ingredients.json'
pk = 0
new_list = []

with open('ingredients.json') as json_data:
    d = json.load(json_data)
    for item in d:
        pk += 1
        item = {"model": "recipes.ingredient", "pk": pk, "fields": item}
        if item not in new_list:
            new_list.append(item)
            json_data.close()


def list_to_json_file(list_of_dicts, file_name):
    with open(file_name+'.json', 'w') as file:
        json.dump(list_of_dicts, file)
    print('{}.Json file created'.format('converted2_my_ingredients'))


list_to_json_file(new_list, 'converted2_my_ingredients')
