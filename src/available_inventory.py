
class InventoryQueries:

    def __init__(self, inventory):
        self.inventory = inventory

    def get_available_inventory(self):
        return self.inventory