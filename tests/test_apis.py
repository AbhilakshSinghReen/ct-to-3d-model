from os.path import basename as path_basename, join as path_join
from sys import stdout
from time import sleep
import unittest

import requests

from dirs import data_dir
from utils import print_inline


class TestAPIs(unittest.TestCase):
    api_base_url = "http://localhost:8000/api"
    test_volume_path = path_join(data_dir, "testing", "volume.nii.gz")


    def test_add_segmentation_task_and_get_result(self):
        add_segmentation_task_endpoint = f"{self.api_base_url}/add-segmentation-task"

        print_inline("Adding task ...")
        
        with open(self.test_volume_path, "rb") as f:
            files = {"file": f}
            add_response = requests.post(add_segmentation_task_endpoint, files=files)

        self.assertEqual(add_response.status_code, 206)
        self.assertEqual(add_response.headers['content-type'], "application/json")

        add_response_data = add_response.json()

        self.assertEqual(add_response_data.get('success', None), True)
        self.assertNotEqual(add_response_data.get('result', {}).get('taskId', None), None)

        print("    ok.")

        task_id = add_response_data['result']['taskId']
        get_segmentation_task_result_endpoint = f"{self.api_base_url}/get-segmentation-task-result?task_id={task_id}"
        expected_volume_file_url = path_join(path_basename(data_dir), task_id, "volume.nii.gz")
        expected_segmentation_file_url = path_join(path_basename(data_dir), task_id, "segmentation.nii.gz")

        print_inline("Getting task status ")

        while True:
            get_result_response = requests.get(get_segmentation_task_result_endpoint)

            self.assertEqual(get_result_response.status_code, 200)
            self.assertEqual(get_result_response.headers['content-type'], "application/json")

            get_result_response_data = get_result_response.json()

            self.assertEqual(get_result_response_data.get('success', None), True)
            self.assertNotEqual(get_result_response_data.get('result', {}).get('status', None), None)
            self.assertEqual(get_result_response_data.get('result', {}).get('taskId', None), task_id)
            self.assertEqual(
                get_result_response_data.get('result', {}).get('volumeFileUrl', None),
                expected_volume_file_url
            )

            print_inline(".")

            if get_result_response_data['result']['status'] == "failed":
                self.fail("Server failed to segment the uploaded volume.")
                break

            if get_result_response_data['result']['status'] == "completed":
                self.assertEqual(
                    get_result_response_data.get('result', {}).get('segmentationFileUrl', None).strip(),
                    expected_segmentation_file_url.strip()
                )
                break

            sleep(1)


if __name__ == "__main__":
    unittest.main()
