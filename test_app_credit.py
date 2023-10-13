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


def test_post_refused(app, client):
    test_body = df.iloc[0].to_dict()
    res = client.post(URL_POST, data=json.dumps(test_body), content_type='application/json')
    assert res.status_code == 200
    expected = {'credit_granted': 'no',
                'credit_proba_limit': 0.54,
                'probability': 0.42
                }

    assert expected == json.loads(res.get_data(as_text=True))


def test_post(app, client):
    test_body = df.iloc[4].to_dict()
    res = client.post(URL_POST, data=json.dumps(test_body), content_type='application/json')
    assert res.status_code == 200
    expected = {'credit_granted': 'yes',
                'credit_proba_limit': 0.54,
                'probability': 0.88
                }

    assert expected == json.loads(res.get_data(as_text=True))
