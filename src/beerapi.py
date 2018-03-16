import requests
import datetime
import time
import logging
def write_beer_inventory():
    """
    Retrieves inventory data from Tanczos and writes to file locally

    Input:
        None

    Output:
        Returns void

    Raises:
    Exception
        When unable to fetch file, logs error and passes
    """
    try:
        beer_inventory = requests.get('http://www.tanczos.com/tanczos.com/beerinventory/webexport.csv')
        filename = str(datetime.datetime.now()).replace(' ', '_') + '.csv'
        with open(filename, "w+") as beer_inventory_file:
            beer_inventory_file.write(beer_inventory.text)
        logging.info('The data was fetched successfully!')

    except OSError as e:
        error_subclass = type(e).__name__
        logging.exception('Failed to fetch file: {}'.format(error_subclass))
        pass

    except requests.exceptions.ConnectionError as err:
        error = str(err).split(':')
        arrayLen = len(error)
        error_msg = format(type(err).__name__) + " " + error[arrayLen - 2][1:] + ":" + error[arrayLen - 1][:-4] + ")"
        logging.warning(error_msg)
        pass

def run():
    """
    Runs write_beer_inventory every 20 minutes

    Input:
        None

    Output:
        Returns void
    """
    seconds_between_fetches = 1200

    while True:
        write_beer_inventory()
        time.sleep(seconds_between_fetches)

if __name__ == "__main__":
    logging.basicConfig(filename='abv.log', level=logging.INFO, format='%(asctime)s:%(message)s')
    run()
