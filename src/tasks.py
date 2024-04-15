from os import environ
from os.path import join as path_join
from subprocess import run as subprocess_run, CalledProcessError
from time import sleep

from huey import RedisHuey

from src.redis_client import redis_client
from src.dirs import data_dir


redis_host = environ["REDIS_HOST"]
task_delay = float(environ.get("TASK_DELAY", 0))

huey = RedisHuey('entrypoint', host=redis_host)

task_status_map_name = "segmentation_task_status"


@huey.task()
def segment_volume(task_id):
    volume_path = path_join(data_dir, task_id, "volume.nii.gz")
    
    redis_client.hset(task_status_map_name, task_id, "processing")

    # Segment the volume
    run_total_segmentator_command = f"cp {path_join(data_dir, 'testing', 'segmentation.nii.gz')} {path_join(data_dir, task_id)}"
    sleep(15)
    # TotalSegmentator -i 1.nii.gz -o 1-tsoc.nii.gz --ml

    try:
        _result = subprocess_run(run_total_segmentator_command, shell=True, check=True)
        redis_client.hset(task_status_map_name, task_id, "completed")
    except CalledProcessError as e:
        print(f"Failed to segment volume for task_id {task_id}.")
        print(f"    segmentation command: {run_total_segmentator_command}")
        redis_client.hset(task_status_map_name, task_id, "failed")
    