import os

from flask_restful import Resource
from flask import request, send_file, Response
from common.config import UPLOAD_FOLDER
import boto3
import requests
from io import BytesIO

s3 = boto3.client("s3")
BUCKET_NAME = "holloo-kiosk-test-1"


class FileUploader(Resource):
    def get(self):
        user_id = request.args.get("user_id")
        folder = request.args.get("folder")
        file = request.args.get("file")
        if not file:
            return "file is missing", 500

        # s3_response = s3.get_object(
        #     Bucket=BUCKET_NAME, Key=f"data/{user_id}/{folder}/{file}"
        # )
        # image_data = s3_response["Body"].read()  # read image bytes

        # return Response(image_data, mimetype="image/jpeg")

        image_url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": f"data/{user_id}/{folder}/{file}",
            },
            ExpiresIn=3600,
        )

        return image_url, 200

        try:
            # Fetch the image from the URL
            resp = requests.get(image_url)
            resp.raise_for_status()  # raise error if failed

            # Wrap content in BytesIO so Flask can send it as a file
            return send_file(
                BytesIO(resp.content),
                mimetype=resp.headers.get("Content-Type", "image/jpeg"),
            )

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

        return image_url, 200

    def post(self):
        user_id = request.args.get("user_id")
        if not user_id:
            return "user id is missing", 500

        folder = request.args.get("folder")
        if not folder:
            return "folder is missing", 500

        if "file" not in request.files:
            return "file type is missing", 500

        if not os.path.exists(os.path.join(UPLOAD_FOLDER, user_id)):
            os.makedirs(os.path.join(UPLOAD_FOLDER, user_id))

        if not os.path.exists(os.path.join(UPLOAD_FOLDER, user_id, folder)):
            os.makedirs(os.path.join(UPLOAD_FOLDER, user_id, folder))

        files = request.files.getlist("file")

        for file in files:
            # ADD FILE TO S3 BUCKET
            try:
                # Upload file directly to S3
                s3.upload_fileobj(
                    file,  # file object from Flask
                    BUCKET_NAME,
                    f"data/{user_id}/{folder}/{file.filename}",  # S3 key (path in bucket)
                )

                file_url = (
                    f"https://{BUCKET_NAME}.s3.amazonaws.com/uploads/{file.filename}"
                )

                return ({"message": "Upload successful", "url": file_url}), 200

            except Exception as e:
                return ({"error": str(e)}), 500

            # Save FILE TO SYSTEM
            file.save(os.path.join(UPLOAD_FOLDER, user_id, folder, file.filename))

        return "upload ok", 200
