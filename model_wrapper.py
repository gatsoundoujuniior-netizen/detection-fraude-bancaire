class RFWithThreshold:
    def __init__(self, rf_model, threshold=0.35, alert_threshold=0.8):
        self.rf_model = rf_model
        self.threshold = threshold
        self.alert_threshold = alert_threshold
    
    def predict(self, X):
        y_proba = self.rf_model.predict_proba(X)[:, 1]
        predictions = (y_proba >= self.threshold).astype(int)

        alert_flags = y_proba >= self.alert_threshold

        return {
            "predictions": predictions,
            "probabilities": y_proba,
            "alerts": alert_flags
        }
