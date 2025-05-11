from src.config import ROOT_DIR
import pickle

import pandas as pd
import numpy as np


CHECKPOINTS_DIRECTORY = ROOT_DIR / "ml/checkpoints"

with open(CHECKPOINTS_DIRECTORY / "lr.pkl", "rb") as f:
    lr = pickle.load(f)

with open(CHECKPOINTS_DIRECTORY / "gb.pkl", "rb") as f:
    gb = pickle.load(f)

with open(CHECKPOINTS_DIRECTORY / "rf.pkl", "rb") as f:
    rf = pickle.load(f)

with open(CHECKPOINTS_DIRECTORY / "label_encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

with open(CHECKPOINTS_DIRECTORY / "scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

categorical_columns = ['fueltype', 'aspiration', 'doornumber', 'carbody', 'drivewheel',
                       'enginelocation', 'enginetype', 'cylindernumber', 'fuelsystem', 'brand', 'model']
numerical_columns = ['wheelbase', 'carlength', 'carwidth', 'carheight', 'curbweight',
                     'enginesize', 'boreratio', 'stroke', 'compressionratio', 'horsepower',
                     'peakrpm', 'citympg', 'highwaympg']

MODEL_NAME_TO_OBJECT = {
    "linear_regression": lr,
    "gradient_boosting": gb,
    "random_forest": rf
}


def predict(model_name: str, data: dict) -> float:
    model = MODEL_NAME_TO_OBJECT[model_name]
    
    data = {k: [v] for k, v in data.items()}
    data = pd.DataFrame.from_dict(data)

    for column in categorical_columns:
        data[column] = encoders[column].transform(data[column])

    data['power_to_weight_ratio'] = data['horsepower'] / data['curbweight']
    for column in numerical_columns:
        data[f'{column}_squared'] = data[column] ** 2

    data['log_enginesize'] = np.log(data['enginesize'].astype("float") + 1)

    data[numerical_columns] = scaler.transform(data[numerical_columns])

    return model.predict(data)[0]
