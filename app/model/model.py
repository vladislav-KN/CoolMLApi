from sklearn.ensemble import GradientBoostingClassifier
import pickle



class Model:
    def __init__(self, model_path=None):
        self.model = GradientBoostingClassifier()
        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path):
        with open(model_path, 'rb') as classifier_file:
            self.model = pickle.load(classifier_file)

    def save_model(self, model_path):
        with open(model_path, 'wb') as classifier_file:
            pickle.dump(self.model, classifier_file)


