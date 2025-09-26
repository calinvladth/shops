import os
import time

from werkzeug.utils import secure_filename
from common.config import UPLOAD_FOLDER, UPLOAD_FOLDER_NAME


def save_file(file):
    timestamp = time.time()
    ext = os.path.splitext(file.filename)[1]
    filename = secure_filename(f"{timestamp}{ext}")
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(save_path)

    url_path = f"/{UPLOAD_FOLDER_NAME}/{filename}"

    return filename, url_path


def remove_file(file):
    if os.path.exists(os.path.join(UPLOAD_FOLDER, file.filename)):
        os.remove(os.path.join(UPLOAD_FOLDER, file.filename))
