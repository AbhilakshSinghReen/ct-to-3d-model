from os.path import dirname, join as path_join


src_dir = dirname(__file__)
server_worker_dir = dirname(src_dir)
project_dir = dirname(server_worker_dir)
data_dir = path_join(project_dir, "data")
