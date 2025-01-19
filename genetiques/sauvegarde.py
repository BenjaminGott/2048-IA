import json


def save_pop(population, generation, file_name="pop.json"):
    with open(file_name, 'w') as f:
        json.dump({{generation}: generation, "population": population},f)
        
        
        
def load_pop(file_name="pop.json"):
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
            return data["population"], data["generation"]
    except FileNotFoundError:
        print("File not found, new population ")
        return [],0