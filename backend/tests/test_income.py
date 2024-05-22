from fastapi.testclient import TestClient

def test_find_all(client_fixture: TestClient):
    response = client_fixture.get('/incomes')
    assert response.status_code == 200
    incomes = response.json()
    assert len(incomes) == 2

def test_find_by_id_正常系(client_fixture: TestClient):
    response = client_fixture.get('/incomes/1')
    assert response.status_code == 200
    income = response.json()
    assert income['id'] == 1

def test_find_by_id_異常系(client_fixture: TestClient):
    response = client_fixture.get('/incomes/10')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Income not found'

def test_find_by_description(client_fixture: TestClient):
    response = client_fixture.get("/incomes/?description=test1")
    assert response.status_code == 200
    income = response.json()
    assert len(income) == 1
    assert income[0]['description'] == 'test1'

def test_find_by_year(client_fixture: TestClient):
    response = client_fixture.get("/incomes/year/2024")
    assert response.status_code == 200
    income = response.json()
    assert len(income) == 1
    assert income[0]['year'] == '2024'

def test_create(client_fixture: TestClient):
    response = client_fixture.post('/incomes', json={'description': 'test3', 'price': 3000000, 'user_id': 1})
    assert response.status_code == 201
    income = response.json()
    assert income['id'] == 3
    assert income['price'] == 3000000
    assert income['description'] == 'test3'

    response = client_fixture.get('/incomes')
    assert len(response.json()) == 3

def test_update_正常系(client_fixture: TestClient):
    response = client_fixture.put('/incomes/1', json={'description': 'update_test1', 'price': 4000000})
    assert response.status_code == 200
    income = response.json()
    assert income['price'] == 4000000
    assert income['description'] == 'update_test1'

def test_update_異常系(client_fixture: TestClient):
    response = client_fixture.put('/incomes/10', json={'description': 'update_test1', 'price': 4000000})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Income not updated'

def test_delete_正常系(client_fixture: TestClient):
    response = client_fixture.delete('/incomes/1')
    assert response.status_code == 200
    response = client_fixture.get('/incomes')
    assert len(response.json()) == 1

def test_delete_異常系(client_fixture: TestClient):
    response = client_fixture.delete('/incomes/10')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Income not deleted'
    response = client_fixture.get('/incomes')
    assert len(response.json()) == 2