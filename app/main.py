import os
from flask import Flask, request
from flask_restful import Resource, Api

cwd = os.getcwd()
UPLOAD_FOLDER = "data"

app = Flask(
    __name__,
    static_folder=os.path.join(cwd, UPLOAD_FOLDER),
)
app.config["UPLOAD_FOLDER"] = os.path.join(cwd, UPLOAD_FOLDER)
api = Api(app)


class FileUploader(Resource):
    def get(self):
        user_id = request.args.get("user_id")
        if not user_id:
            return "user id is missing", 500

        folder = request.args.get("folder")
        if not folder:
            return "folder is missing", 500

        return "get file", 200

    def post(self):
        user_id = request.args.get("user_id")
        if not user_id:
            return "user id is missing", 500

        folder = request.args.get("folder")
        if not folder:
            return "folder is missing", 500

        if "file" not in request.files:
            return "file type is missing", 500

        if not os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], user_id)):
            os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], user_id))

        if not os.path.exists(
            os.path.join(app.config["UPLOAD_FOLDER"], user_id, folder)
        ):
            os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], user_id, folder))

        files = request.files.getlist("file")

        for file in files:
            file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"], user_id, folder, file.filename
                )
            )

        return "upload ok", 200


api.add_resource(FileUploader, "/upload")

if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    app.run(port=8000, debug=True)
