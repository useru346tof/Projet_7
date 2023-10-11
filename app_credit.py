import os

import numpy as np
from flask import Flask, jsonify, request, config, Response, json
import skops.io as sio
from lightgbm import LGBMClassifier

app = Flask(__name__)
model = sio.load('final_model_GBM.skops', trusted=True)
tresh = 0.42

def transform_data(dictionnaire):
    result = dictionnaire.values()
    # Convert object to a list
    data = list(result)
    # Convert list to an array
    numpyArray = np.array(data)
    transformed_data = numpyArray.reshape(1,-1).astype('float64')
    return transformed_data


@app.route('/api/credit/', methods=['POST'])
def allow_credit_post():
    args = request.get_json()
    if type(args) is not dict:
        args = json.loads(args)
    if 'Unnamed: 0' in args:
        args.pop('Unnamed: 0')
    transformed = transform_data(args)
    result_proba = model.predict_proba(transformed)
    result_proba = round(result_proba[0,0], 2)
    if (result_proba) < tresh:
        granted = 'no'
    else:
        granted = 'yes'
    credit_prediction = {
        'probability': result_proba,
        'credit_granted': granted,
        'credit_proba_limit': tresh
    }
    return jsonify(credit_prediction)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

