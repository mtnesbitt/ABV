
from available_inventory import InventoryQueries


def test_no_inventory():
    queries = InventoryQueries([])
    assert [] == queries.get_available_inventory()


def test_single_item():
    expected = {'name': 'Bells Best Brown',
                'size': '1/4 Keg',
                'style': 'Craft',
                'quantity': 1,
                'price': 118.99}

    inventory = [expected]

    queries = InventoryQueries(inventory)
    assert [expected] == queries.get_available_inventory()