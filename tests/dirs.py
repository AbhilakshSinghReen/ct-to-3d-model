from os import makedirs
from os.path import dirname, join as path_join


tests_dir = dirname(__file__)
project_dir = dirname(tests_dir)
data_dir = path_join(project_dir, "data")

makedirs(data_dir, exist_ok=True)
