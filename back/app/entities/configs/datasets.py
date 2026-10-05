from pathlib import Path

DATASET_DIR = Path(__file__).resolve().parents[2] / "datasets"

class Datasets:
    """
    Class to define paths to various datasets.
    """

    raw_ckd = str(DATASET_DIR / 'raw' / 'ckd.csv')
    raw_disease = str(DATASET_DIR / 'raw' / 'disease.csv')
    raw_cassi = str(DATASET_DIR / 'raw' / 'ca_ssi_adult_odp_2022.csv')
    raw_maternal = str(DATASET_DIR / 'raw' / 'maternal_health_risk.csv')

    ckd = str(DATASET_DIR / 'clean' / 'ckd.csv')
    disease = str(DATASET_DIR / 'clean' / 'disease.csv')
    cassi = str(DATASET_DIR / 'clean' / 'ca_ssi_adult_odp_2022.csv')
    maternal = str(DATASET_DIR / 'clean' / 'maternal_health_risk.csv')

    ckd_train = 'ckd'
    disease_train = 'Critical'
    cassi_train = 'SIR'
    maternal_train = 'RiskLevel'

    @classmethod
    def get_raw_dataset(cls, dataset_name):
        """
        Method to retrieve the path of a raw dataset based on its name.

        Args:
        dataset_name (str): The name of the raw dataset.

        Returns:
        str: The path to the raw dataset.
        """
        return getattr(cls, f'raw_{dataset_name.lower()}')

    @classmethod
    def get_clean_dataset(cls, dataset_name):
        """
        Method to retrieve the path of a clean dataset based on its name.

        Args:
        dataset_name (str): The name of the clean dataset.

        Returns:
        str: The path to the clean dataset.
        """
        return getattr(cls, dataset_name.lower())

    @classmethod
    def get_train_label(cls, dataset_name):
        """
        Method to retrieve the training label for a dataset.

        Args:
        dataset_name (str): The name of the dataset.

        Returns:
        str: The training label for the dataset.
        """
        return getattr(cls, f'{dataset_name.lower()}_train')