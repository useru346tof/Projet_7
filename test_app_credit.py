import json

import numpy as np
import pytest
import pandas as pd

from app_credit import transform_data
from app_credit import app as flask_app
from fixtures import TEST_DICTIONNAIRE, RESULT_TEST_DICT, URL_POST, BODY_POST

df = pd.read_csv("test_dataframe.csv")


def test_transformed_data_ok():
    assert transform_data({'test': '0.1'}) == [[0.1]]


def test_transformed_data_ok_2():
    assert np.testing.assert_array_equal(transform_data(TEST_DICTIONNAIRE), RESULT_TEST_DICT) == None


def test_post(app, client):
    test_body = df.iloc[0].to_dict()
    res = client.post(URL_POST, data=json.dumps(test_body), content_type='application/json')
    assert res.status_code == 200
    expected = {'credit_granted': 'yes',
                'credit_proba_limit': 0.42,
                'probability': 0.5
                }

    assert expected == json.loads(res.get_data(as_text=True))

'''
class TestAppCredit(pytest.TestCase):

    def test_transformed_data_ok(self):
        self.assertIsNone(np.testing.assert_array_equal(transform_data({'test': '0.1'}), [[0.1]]))

    def test_transformed_data_ok_2(self):
        #print(transform_data(TEST_DICTIONNAIRE), RESULT_TEST_DICT)
        self.assertIsNone(np.testing.assert_array_equal(transform_data(TEST_DICTIONNAIRE), RESULT_TEST_DICT))

'''

'''
@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_should_status_code_ok(client):
    response = client.get('/api/credit/')
    assert response.status_code == 200
'''

'''
if __name__ == '__main__':
    unittest.main()
    '''