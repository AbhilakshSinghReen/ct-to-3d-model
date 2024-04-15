from os.path import join as path_join
import unittest

import requests

from dirs import data_dir


class TestAPIs(unittest.TestCase):
    api_base_url = "http://localhost:8000/api"
    test_volume_path = path_join(data_dir, "testing", "volume.nii.gz")


    def test_add_segmentation_task_and_get_result(self):
        add_segmentation_task_endpoint = f"{self.api_base_url}/add-segmentation-task"

        with open(self.test_volume_path, "rb") as f:
            files = {"file": f}
            response = requests.post(add_segmentation_task_endpoint, files=files)

        self.assertEqual(response.status_code, 206)


if __name__ == "__main__":
    unittest.main()
