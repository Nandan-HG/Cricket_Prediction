
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def fit_regression_models(metrics, target):
    data = metrics[
        ["ball_faced_number", target, "batter_innings"]
    ].dropna().copy()

    data = data[data["batter_innings"] >= 50]

    if len(data) < 10:
        raise ValueError("Not enough data to fit regression models.")

    X = data[["ball_faced_number"]]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Polynomial Regression": make_pipeline(
            PolynomialFeatures(degree=2, include_bias=False),
            LinearRegression()
        )
    }

    results = []

    for name, model in models.items():
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        results.append({
            "Model": name,
            "Test R2": r2_score(y_test, predictions),
            "Test RMSE": np.sqrt(
                mean_squared_error(y_test, predictions)
            )
        })

    # Fit the models on all available points for visualization.
    for model in models.values():
        model.fit(X, y)

    X_curve = pd.DataFrame({
        "ball_faced_number": np.arange(
            int(X["ball_faced_number"].min()),
            int(X["ball_faced_number"].max()) + 1
        )
    })

    curve = X_curve.copy()
    curve["Linear"] = models["Linear Regression"].predict(X_curve)
    curve["Polynomial"] = models["Polynomial Regression"].predict(
        X_curve
    )

    return pd.DataFrame(results), curve
