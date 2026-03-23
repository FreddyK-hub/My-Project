from __future__ import annotations

import numpy as np


class AirlinePassengerForecaster:
    """
    A deployable lag-based forecaster derived from the Airline Passengers assignment.
    It uses the previous 12 monthly values to predict the next month.

    This version uses a compact linear model on lag features so the service is easy
    to deploy reliably on free hosting. The interface is the same one you would use
    for an LSTM-backed service.
    """

    model_name = "Lag-12 linear regression forecaster"

    def __init__(self) -> None:
        self.lookback = 12
        self.train_series = np.array([
            112,118,132,129,121,135,148,148,136,119,104,118,
            115,126,141,135,125,149,170,170,158,133,114,140,
            145,150,178,163,172,178,199,199,184,162,146,166,
            171,180,193,181,183,218,230,242,209,191,172,194,
            196,196,236,235,229,243,264,272,237,211,180,201,
            204,188,235,227,234,264,302,293,259,229,203,229,
            242,233,267,269,270,315,364,347,312,274,237,278,
            284,277,317,313,318,374,413,405,355,306,271,306,
            315,301,356,348,355,422,465,467,404,347,305,336,
            340,318,362,348,363,435,491,505,404,359,310,337,
            360,342,406,396,420,472,548,559,463,407,362,405,
            417,391,419,461,472,535,622,606,508,461,390,432,
        ], dtype=float)
        self.intercept, self.coef_ = self._fit_from_series(self.train_series, self.lookback)

    @staticmethod
    def _fit_from_series(series: np.ndarray, lookback: int) -> tuple[float, np.ndarray]:
        X, y = [], []
        for i in range(len(series) - lookback):
            X.append(series[i:i+lookback])
            y.append(series[i+lookback])
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        X_design = np.column_stack([np.ones(len(X)), X])
        beta, *_ = np.linalg.lstsq(X_design, y, rcond=None)
        return float(beta[0]), beta[1:]

    def predict_next(self, history: list[float]) -> float:
        if len(history) != self.lookback:
            raise ValueError(f"Expected exactly {self.lookback} months of history.")
        x = np.asarray(history, dtype=float)
        if np.any(x < 0):
            raise ValueError("Passenger counts must be non-negative.")
        pred = self.intercept + float(np.dot(self.coef_, x))
        return max(pred, 0.0)
