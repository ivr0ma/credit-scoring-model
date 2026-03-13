import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import os


class CreditScoringModel:
    def __init__(self):
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42,
        )
        self.scaler = StandardScaler()
        self._train()

    def _train(self):
        np.random.seed(42)
        n_samples = 1000

        age = np.random.randint(18, 70, n_samples)
        income = np.random.uniform(20000, 200000, n_samples)
        loan_amount = np.random.uniform(1000, 100000, n_samples)
        loan_term = np.random.randint(6, 360, n_samples)
        credit_history = np.random.randint(0, 240, n_samples)
        num_lines = np.random.randint(0, 20, n_samples)
        employment_years = np.random.uniform(0, 40, n_samples)
        dti = np.random.uniform(0, 0.8, n_samples)

        X = np.column_stack([
            age, income, loan_amount, loan_term,
            credit_history, num_lines, employment_years, dti
        ])

        score = (
            0.2 * (income / 200000)
            + 0.2 * (credit_history / 240)
            + 0.15 * (employment_years / 40)
            - 0.2 * (loan_amount / 100000)
            - 0.15 * dti
            + 0.1 * np.random.random(n_samples)
        )
        y = (score > 0.3).astype(int)

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]
