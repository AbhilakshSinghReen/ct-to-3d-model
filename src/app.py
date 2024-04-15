from os import makedirs
from os.path import basename as path_basename, join as path_join
from uuid import uuid4

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

from src.dirs import data_dir
from src.redis_client import redis_client
from src.tasks import segment_volume, task_status_map_name


app = FastAPI()


@app.post("/api/add-segmentation-task")
async def upload_file(file: UploadFile = File(...)):
    task_id = str(uuid4())
    task_dir = path_join(data_dir, task_id)
    makedirs(task_dir)

    volume_save_path = path_join(task_dir, "volume.nii.gz")

    # Save the file to the disk
    with open(volume_save_path, "wb") as buffer:
        while True:
            chunk = await file.read(10000)
            if not chunk:
                break

            buffer.write(chunk)
    
    # Queue the task
    redis_client.hset(task_status_map_name, task_id, "queued")
    segment_volume(task_id)

    return JSONResponse(content={
        'success': True,
        'result': {
            'taskId': task_id,
        },
    }, status_code=206)


@app.get("/api/get-segmentation-task-result")
async def get_segmentation(task_id: str):
    task_status = redis_client.hget(task_status_map_name, task_id)

    response_content = {
        'success': True,
        'result': {
            'taskId': task_id,
            'status': task_status,
            'volumeFileUrl': path_join(path_basename(data_dir), task_id, "volume.nii.gz"),
        },
    }
    
    if task_status == "completed":
        response_content['result']['segmentationFileUrl'] = path_join(path_basename(data_dir), task_id, "segmentation.nii.gz")
    
    return JSONResponse(content=response_content, status_code=200)
