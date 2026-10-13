import pandas as pd
import os

DATASET_PATH = os.path.join(os.path.dirname(__file__), "../../data/Social Media Engagement Dataset.csv")

class DataRepository:
    _instance = None
    df = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataRepository, cls).__new__(cls)
            cls._instance.load_data()
        return cls._instance

    def load_data(self):
        if os.path.exists(DATASET_PATH):
            self.df = pd.read_csv(DATASET_PATH)
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            print(f"[Dataset Loaded]: {len(self.df)} records successfully initialized.")
        else:
            raise FileNotFoundError(f"Dataset not found at path: {DATASET_PATH}")

    def get_data(self):
        return self.df