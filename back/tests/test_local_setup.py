import unittest
from pathlib import Path
from unittest.mock import Mock

from pydantic import ValidationError
from app.entities.configs.datasets import Datasets
from app.entities.requests.risk_assessment_request import RiskAssessmentRequest
from app.services.utils.mapper import Mapper
from app.dal.proxys.account_proxy import AccountProxy


class LocalSetupTests(unittest.TestCase):
    def test_dataset_paths_exist_without_changing_directory(self):
        for name in ("raw_ckd", "raw_disease", "raw_cassi", "raw_maternal"):
            self.assertTrue(Path(getattr(Datasets, name)).is_file())
            self.assertTrue(Path(getattr(Datasets, name)).is_absolute())

    def test_decimal_and_blank_measurements(self):
        request = RiskAssessmentRequest(
            name="Demo", age="30", bloodSugar="5.5", bodyTemperature="37.5",
            bloodPressure="", disease="", diseaseRating=1, ckdRating=1,
            sirRating=1, maRating=1,
        )
        mapped = Mapper().map_to_risk_assessment_request(request)
        self.assertEqual(mapped["Blood Sugar"], 5.5)
        self.assertEqual(mapped["Body Temperature"], 37.5)
        self.assertIsNone(mapped["Blood Pressure"])
        self.assertIsNone(mapped["Disease"])

    def test_invalid_measurements_and_ratings_are_rejected(self):
        base = dict(name="Demo", diseaseRating=1, ckdRating=1, sirRating=1, maRating=1)
        for invalid in ({"bloodSugar": "invalid"}, {"maRating": 6}, {"bodyTemperature": "NaN"}):
            with self.assertRaises(ValidationError):
                RiskAssessmentRequest(**(base | invalid))

    def test_failed_save_rolls_back_and_raises(self):
        proxy = AccountProxy.__new__(AccountProxy)
        proxy.db = Mock()
        proxy.db.cursor.return_value.execute.side_effect = RuntimeError("insert failed")
        with self.assertRaisesRegex(RuntimeError, "insert failed"):
            proxy.create_patient("Demo", 30, "", "", "demo@example.com", 1)
        proxy.db.rollback.assert_called_once()
        proxy.db.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
