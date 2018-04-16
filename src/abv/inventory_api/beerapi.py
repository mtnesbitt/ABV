from flask import Flask, request
from abv.inventory_api.inventory import Inventory
from abv.inventory_api.inventory_queries import InventoryQueries
from abv.inventory_api.filter_ds import FilterDS
import json
app = Flask(__name__)

inventory = None #Inventory("../../tests/sample_csv_files/three_two_positive_one_negative.csv")
queries = InventoryQueries(inventory)

@app.route('/current')
def get_current_inventory():

    name = request.args.get('name')
    size = request.args.get('size')
    style = request.args.get('style')
    availability = request.args.get('availability')

    filter = FilterDS(name=name, size=size, style=style, availability=availability)
    beers = []
    filtered_inventory = queries.get_filtered_inventory(filter)
    if filtered_inventory:
        for beer in filtered_inventory:
            beers.append({'name': beer.name, 'size': beer.size, 'style': beer.style, 'quantity': beer.quantity,
                          'price': beer.price})
        return json.dumps(beers)

    else:
        return json.dumps([])


if __name__ == "__main__":
    app.run(host="localhost")