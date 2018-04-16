from tests.inventory_api_tests.mock_inventory_queries import MockInventoryQueries
from abv.inventory_api.beer import Beer
import abv.inventory_api.beerapi as beerapi
from tests.inventory_api_tests.mock_inventory_queries_saving import MockInventoryQueriesSaving

beerapi.app.testing = True
app = beerapi.app.test_client()

def test_empty_results():
    beerapi.queries = MockInventoryQueries([])
    result = app.get('/current')
    assert result.data == b'[]'

def test_single_result():
    pabst = Beer(name='Pabst', size='12/12oz', style='lager',quantity='1', price='20')
    beerapi.queries = MockInventoryQueries([pabst])
    result = app.get('/current')
    assert result.data == b'[{"name": "Pabst", "size": "12/12oz", "style": "lager", "quantity": "1", "price": "20"}]'

def test_two_results():
    pabst = Beer(name='Pabst', size='12/12oz', style='lager',quantity='1', price='20')
    guinness = Beer(name='Guinness', size='12/12oz', style='lager', quantity='1', price='20')
    beerapi.queries = MockInventoryQueries([pabst, guinness])
    result = app.get('/current')
    assert result.data == b'[{"name": "Pabst", "size": "12/12oz", "style": "lager", "quantity": "1", "price": "20"}, ' \
                          b'{"name": "Guinness", "size": "12/12oz", "style": "lager", "quantity": "1", "price": "20"}]'

def test_no_filter():
    saver = MockInventoryQueriesSaving()
    beerapi.queries = saver
    app.get('/current')
    assert saver.filter.name is None
    assert saver.filter.style is None

def test_name_filter():
    saver = MockInventoryQueriesSaving()
    beerapi.queries = saver
    app.get('/current?name=Guinness')
    assert saver.filter.name == 'Guinness'
    assert saver.filter.style is None

def test_availability_filter():
    saver = MockInventoryQueriesSaving()
    beerapi.queries = saver
    app.get('/current?name=Guinness&availability=2')
    assert saver.filter.name == 'Guinness'
    assert saver.filter.availability == '2'
    assert saver.filter.style == None

def test_style_filter():
    saver = MockInventoryQueriesSaving()
    beerapi.queries = saver
    app.get('/current?name=Guinness&availability=2&style=stout')
    assert saver.filter.name == 'Guinness'
    assert saver.filter.availability == '2'
    assert saver.filter.style == 'stout'
    assert saver.filter.size is None

def test_size_filter():
    saver = MockInventoryQueriesSaving()
    beerapi.queries = saver
    app.get('/current?name=Guinness&availability=2&style=stout&size=12/12OZ')
    assert saver.filter.name == 'Guinness'
    assert saver.filter.availability == '2'
    assert saver.filter.style == 'stout'
    assert saver.filter.size == '12/12OZ'

def test_bad_params():
    saver = MockInventoryQueriesSaving()
    beerapi.queries = saver
    result = app.get('/current?foo=bar')
    assert result.status_code is 200
    assert saver.filter.style is None
    assert saver.filter.name is None
    assert saver.filter.size is None
    assert saver.filter.availability is None

def test_bad_and_good_params():
    saver = MockInventoryQueriesSaving()
    beerapi.queries = saver
    result = app.get('/current?name=Guinness&foo=bar')
    assert result.status_code is 200
    assert saver.filter.name == 'Guinness'

def test_repeat_param():
    saver = MockInventoryQueriesSaving()
    beerapi.queries = saver
    result = app.get('/current?name=beer&name=beer')
    assert result.status_code is 200
    assert saver.filter.name == 'beer'

def test_repeat_params_different_values():
    saver = MockInventoryQueriesSaving()
    beerapi.queries = saver
    result = app.get('/current?name=Pabst&name=Guinness')
    assert result.status_code is 200
    assert saver.filter.name == 'Pabst'
