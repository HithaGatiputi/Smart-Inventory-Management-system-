
from xgboost import XGBClassifier

class XGBoostForecastModel:

    def __init__(self):

        self.model = XGBClassifier(
            n_estimators=200,
            max_depth=6
        )
