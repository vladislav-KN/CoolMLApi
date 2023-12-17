import numpy as np

from app.model.model import Model


class ModelPredictor(Model):
    def __init__(self, model_path=None):
        super().__init__(model_path)

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)[:,1]