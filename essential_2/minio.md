###  Step 1: Download MinIO
```
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo mv minio /usr/local/bin/
```
### Step 2: Set Environment Variables (Access/Secret Key)
```
export MINIO_ROOT_USER=minioadmin
export MINIO_ROOT_PASSWORD=minioadmin123

```

### Step 3: Start MinIO Server
```
minio server ~/minio-data --console-address ":9001"
```
- MinIO API available at: http://localhost:9000

- Web UI (Console): http://localhost:9001

###  Step 4: Access Web UI
```
http://localhost:9001
Login using:
Username: minioadmin
Password: minioadmin123
 ```




 #### Script for checking MinIO upload logs: upload.py


 ```
 import cv2
import os
import time
import threading
import logging
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from minio import Minio
from minio.error import S3Error
from io import BytesIO
from pathlib import Path
import socket


# Create logs directory if not exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Create a new log file with timestamp
hostname = socket.gethostname()
log_filename = LOG_DIR / f"run_{hostname}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# ---- Configuration ----
VIDEO_SOURCE = "Audi_A5_5min_1.mp4"  # local file or RTSP URL
FPS = 10
UPLOAD_DURATION = 10  # seconds (only for RTSP)
MINIO_CONFIG = {
    "endpoint": "192.168.103.194:9000",
    "access_key": "minioadmin",
    "secret_key": "minioadmin123",
    "secure": False,
    "bucket": "forazi"
}
NUM_THREADS = 2
PROGRESS_INTERVAL = 10  # seconds
RETRY_COUNT = 3

# ---- Logging ----
# Create log handlers
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define log format
formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Set up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(console_handler)


# ---- Globals ----
stats = {
    "frames_extracted": 0,
    "uploads_completed": 0,
    "uploads_failed": 0,
    "start_time": time.time()
}
thread_stats = {}  # {thread_id: {"success": 0, "fail": 0}}
lock = threading.Lock()


def is_rtsp(url):
    return url.startswith("rtsp://")


def get_output_key_prefix(video_source):
    if is_rtsp(video_source):
        return f"rtsp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    else:
        return os.path.splitext(os.path.basename(video_source))[0]


def clean_bucket(client, bucket, prefix):
    try:
        objects = client.list_objects(bucket, prefix=prefix, recursive=True)
        for obj in objects:
            client.remove_object(bucket, obj.object_name)
        logger.info(f"Cleared objects with prefix '{prefix}/' in bucket '{bucket}'")
    except S3Error as e:
        logger.error(f"Failed to clean bucket: {e}")


def ensure_bucket(client, bucket):
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)


def upload_image(minio_client, bucket, object_name, image_data):
    for attempt in range(RETRY_COUNT):
        try:
            minio_client.put_object(
                bucket_name=bucket,
                object_name=object_name,
                data=BytesIO(image_data),
                length=len(image_data),
                content_type='image/jpeg'
            )
            with lock:
                stats["uploads_completed"] += 1
                tid = threading.get_ident()
                if tid not in thread_stats:
                    thread_stats[tid] = {"success": 0, "fail": 0}
                thread_stats[tid]["success"] += 1
            return
        except Exception as e:
            logger.warning(f"Upload retry {attempt+1}/{RETRY_COUNT} failed: {object_name}, reason: {e}")
            time.sleep(1)
    with lock:
        stats["uploads_failed"] += 1
        tid = threading.get_ident()
        if tid not in thread_stats:
            thread_stats[tid] = {"success": 0, "fail": 0}
        thread_stats[tid]["fail"] += 1

    logger.error(f"Upload failed after retries: {object_name}")


def progress_logger():
    last_time = stats["start_time"]
    last_extracted = 0
    last_uploaded = 0

    while True:
        time.sleep(PROGRESS_INTERVAL)
        current_time = time.time()
        elapsed = current_time - stats["start_time"]
        interval = current_time - last_time

        with lock:
            total_extracted = stats["frames_extracted"]
            total_uploaded = stats["uploads_completed"]
            total_failed = stats["uploads_failed"]

        delta_extracted = total_extracted - last_extracted
        delta_uploaded = total_uploaded - last_uploaded

        extract_rate = delta_extracted / interval
        upload_rate = delta_uploaded / interval

        logger.info(f"[Progress] Frames Extracted: {total_extracted} "
                    f"(+{delta_extracted}, {extract_rate:.2f}/s), "
                    f"Uploaded: {total_uploaded} "
                    f"(+{delta_uploaded}, {upload_rate:.2f}/s), "
                    f"Failed: {total_failed}, "
                    f"Elapsed: {elapsed:.1f}s")

        last_time = current_time
        last_extracted = total_extracted
        last_uploaded = total_uploaded



def extract_and_upload_frames(video_source, fps, duration=None):
    logger.info("Opening video")
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        logger.error("Failed to open video source.")
        return

    is_stream = is_rtsp(video_source)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if not is_stream else float('inf')
    source_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    interval = int(source_fps / fps)
    prefix = get_output_key_prefix(video_source)

    logger.info("Preparing bucket")
    minio_client = Minio(**{k: MINIO_CONFIG[k] for k in ["endpoint", "access_key", "secret_key", "secure"]})
    ensure_bucket(minio_client, MINIO_CONFIG["bucket"])
    clean_bucket(minio_client, MINIO_CONFIG["bucket"], prefix)

    with lock:
        stats["start_time"] = time.time()
    threading.Thread(target=progress_logger, daemon=True).start()

    logger.info("Starting frame extraction and upload")
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        frame_id = 0
        saved_count = 0
        start = time.time()
        last_log_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_id % interval == 0:
                ts = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                timestamp_str = f"{int(ts//60):02d}_{int(ts%60):02d}_{int((ts%1)*1000):03d}"
                filename = f"{prefix}/frame_{timestamp_str}.jpg"
                success, buffer = cv2.imencode(".jpg", frame)
                if success:
                    futures.append(executor.submit(upload_image, minio_client,
                                                   MINIO_CONFIG["bucket"],
                                                   filename,
                                                   buffer.tobytes()))
                    with lock:
                        stats["frames_extracted"] += 1

            frame_id += 1

            if is_stream and (time.time() - start >= duration):
                break

        with lock:
            stats["extract_end_time"] = time.time()
        logger.info("Frame extraction complete. Waiting for uploads...")

        for f in as_completed(futures):
            pass  # All progress is tracked in upload_image()

    cap.release()


def main():
    # logger.info("Starting frame extraction and upload.")
    # threading.Thread(target=progress_logger, daemon=True).start()
    extract_and_upload_frames(VIDEO_SOURCE, FPS, UPLOAD_DURATION if is_rtsp(VIDEO_SOURCE) else None)
    elapsed = time.time() - stats["start_time"]
    logger.info("----- Summary -----")
    logger.info(f"Total frames extracted: {stats['frames_extracted']}")
    logger.info(f"Total uploaded:         {stats['uploads_completed']}")
    logger.info(f"Total failed:           {stats['uploads_failed']}")
    logger.info(f"Elapsed time:           {elapsed:.2f} seconds")

    extract_duration = stats.get("extract_end_time", stats["start_time"]) - stats["start_time"]
    extract_rate = stats["frames_extracted"] / extract_duration if extract_duration > 0 else 0
    upload_rate = stats["uploads_completed"] / elapsed if elapsed > 0 else 0

    logger.info(f"Average extraction rate: {extract_rate:.2f} frames/sec")
    logger.info(f"Average upload rate:     {upload_rate:.2f} frames/sec")

    if thread_stats:
        logger.info("----- Per-thread Upload Stats -----")
        with lock:
            for tid, counts in thread_stats.items():
                logger.info(f"Thread {tid}: Success = {counts['success']}, Fail = {counts['fail']}")



if __name__ == "__main__":
    main()

```