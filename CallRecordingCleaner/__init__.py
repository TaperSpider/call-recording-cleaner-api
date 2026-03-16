import os
import json
import tempfile
import datetime
import azure.functions as func

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from cleaner.cleaner import process_audio


def main(req: func.HttpRequest) -> func.HttpResponse:

    local_input = None
    cleaned_path = None

    try:

        # -----------------------------
        # Read request body
        # -----------------------------
        req_body = req.get_json()

        storage_account = req_body.get("STORAGE_ACCOUNT")
        container = req_body.get("CONTAINER")
        input_file = req_body.get("INPUT_FILE")

        cleaned_folder_root = req_body.get("CLEANED_RECORDINGS")
        archived_folder_root = req_body.get("ARCHIVED_RECORDINGS")

        if not storage_account or not container:
            return func.HttpResponse(
                json.dumps({"error": "STORAGE_ACCOUNT and CONTAINER are required"}),
                status_code=400,
                mimetype="application/json"
            )

        # -----------------------------
        # Managed Identity Auth
        # -----------------------------
        credential = DefaultAzureCredential()

        blob_service = BlobServiceClient(
            account_url=f"https://{storage_account}.blob.core.windows.net",
            credential=credential
        )

        container_client = blob_service.get_container_client(container)

        # -----------------------------
        # Determine today's folder
        # -----------------------------
        today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

        cleaned_folder = f"{cleaned_folder_root}/{today}"
        archive_folder = f"{archived_folder_root}/{today}"

        # -----------------------------
        # Ensure folders exist
        # -----------------------------
        def ensure_folder(folder):

            blobs = container_client.list_blobs(name_starts_with=f"{folder}/")

            exists = False
            for _ in blobs:
                exists = True
                break

            if not exists:
                placeholder = f"{folder}/.init"
                container_client.upload_blob(placeholder, b"", overwrite=True)

        ensure_folder(cleaned_folder)
        ensure_folder(archive_folder)

        # -----------------------------
        # Download input recording
        # -----------------------------
        file_name = os.path.basename(input_file)

        local_input = os.path.join(tempfile.gettempdir(), file_name)

        with open(local_input, "wb") as f:
            download_stream = container_client.download_blob(input_file)
            f.write(download_stream.readall())

        # -----------------------------
        # Process audio
        # -----------------------------
        cleaned_path, metadata = process_audio(local_input)

        cleaned_name = os.path.basename(cleaned_path)

        cleaned_blob_path = f"{cleaned_folder}/{cleaned_name}"

        # -----------------------------
        # Upload cleaned audio
        # -----------------------------
        with open(cleaned_path, "rb") as data:
            container_client.upload_blob(cleaned_blob_path, data, overwrite=True)

        # -----------------------------
        # Move original file to archive
        # -----------------------------
        archive_blob_path = f"{archive_folder}/{file_name}"

        source_blob = container_client.get_blob_client(input_file)
        archive_blob = container_client.get_blob_client(archive_blob_path)

        archive_blob.start_copy_from_url(source_blob.url)

        source_blob.delete_blob()

        # -----------------------------
        # Response
        # -----------------------------
        response = {
            "input_file": input_file,
            "cleaned_file": cleaned_blob_path,
            "archived_file": archive_blob_path,
            "container": container,
            **metadata
        }

        return func.HttpResponse(
            json.dumps(response),
            mimetype="application/json"
        )

    except Exception as e:

        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

    finally:

        try:
            if local_input and os.path.exists(local_input):
                os.remove(local_input)

            if cleaned_path and os.path.exists(cleaned_path):
                os.remove(cleaned_path)

        except Exception:
            pass