import asyncio
import os

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score, mean_squared_error, r2_score, roc_auc_score, \
    log_loss

from app.model.model import Model


class ModelEducator(Model):
    def __init__(self, model_path=None):
        super().__init__(model_path)

    async def train(self, X_train, y_train, settings: dict, save_to_file = os.path.join(*['app', 'model_files', 'new.pkl'])):
        loop = asyncio.get_event_loop()
        self.model = GradientBoostingClassifier(**settings)
        await loop.run_in_executor(None, self.model.fit, X_train, y_train)
        self.save_model(save_to_file)



    def compute_metrics(self, X, y_true):
        accuracy, recall, f1, mse, r2, auc_roc, log_loss_value = 0, 0, 0, 0, 0, 0, 0
        try:
            y_pred = self.model.predict(X)
            model_type = self.model.__class__.__name__

            if 'Classifier' in model_type:
                # Для классификации
                if hasattr(self.model, 'predict_proba'):
                    y_proba = self.model.predict_proba(X)[:, 1]
                    auc_roc = roc_auc_score(y_true, y_proba)
                    log_loss_value = log_loss(y_true, y_proba)
                else:
                    auc_roc = None
                    log_loss_value = None
            elif 'Regressor' in model_type:
                # Для регрессии
                mse = mean_squared_error(y_true, y_pred)
                r2 = r2_score(y_true, y_pred)

            # Общие метрики для обеих задач
            accuracy = accuracy_score(y_true, y_pred)
            recall = recall_score(y_true, y_pred)
            f1 = f1_score(y_true, y_pred)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            return {
                'Accuracy': accuracy,
                'Recall': recall,
                'F1 Score': f1,
                'Mean Squared Error': mse,
                'R2 Score': r2,
                'AUC-ROC': auc_roc,
                'Log Loss': log_loss_value
            }
