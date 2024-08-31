"""
This module contains functions for interacting with the Google Drive API.
"""

import io
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from googleapiclient.errors import HttpError


def find_file(service, file_name, parent_id, count=0):
    """
    Find a file in Google Drive with the given file name and parent ID.

    Args:
        service (googleapiclient.discovery.Resource): An authenticated Google Drive API
        service object.
        file_name (str): The name of the file to search for.
        parent_id (str): The ID of the parent folder to search in.
        count (int, optional): The number of times the function has been retried (default: 0).

    Returns:
        dict or None: A dictionary representing the file if found, or None if not found.

    Raises:
        HttpError: If an error occurs during the API request.

    Notes:
        - The function retries up to 3 times if an error occurs.
        - The function searches for files with the given name in the specified parent folder.
        - The function returns the first match it finds.
        - The function returns None if no matching file is found.
    """
    try:
        if count >= 3:
            print("Hit max retries for find_file, returning None")
            return None
        # print(f"Searching for {file_name} in {parent_id}")
        query = f"name = '{file_name}' and '{parent_id}' in parents and trashed = false"
        results = (
            service.files()
            .list(
                q=query,
                spaces="drive",
                fields="files(id, name)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            )
            .execute()
        )
        # print(results)
        files = results.get("files", [])
        if files:
            return files[0]  # Return the first match
        return None
    except HttpError as error:
        print(f"An error occurred in find_file - Retying: {error}")
        find_file(service, file_name, parent_id, count + 1)


def export_file(
    service, file_id, mime_type, export_path, folder_id, update_existing, count=0
):
    """
    Export a file from Google Drive.

    Args:
        service (googleapiclient.discovery.Resource): An authenticated Google Drive
        API service object.
        file_id (str): The ID of the file to export.
        mime_type (str): The MIME type of the file.
        export_path (str): The path to export the file to.
        folder_id (str): The ID of the folder to export the file to.
        update_existing (bool): Whether to update an existing file or create a new one.
        count (int, optional): The number of times the function has been retried (default: 0).

    Returns:
        str or None: The ID of the exported file if successful, None if an error occurs.

    Raises:
        HttpError: If an error occurs during the API request.

    Notes:
        - The function retries up to 3 times if an error occurs.
        - If `update_existing` is False, a new file is created to receive the exported content.
        - If `update_existing` is True, the existing file with the specified `file_id` is updated.
        - The exported content is downloaded into an in-memory file-like object before being uploaded
        to the new file.
        - The function prints a message indicating the file that was updated.
    """
    try:
        if count >= 3:
            print("Hit max retries for export_file, returning None")
            return None
        # 1. Initiate the export request
        request = service.files().export_media(fileId=file_id, mimeType=mime_type)

        # 2. Create file metadata for the exported file
        file_metadata = {
            "mimeType": mime_type,
            "name": export_path,
            "parents": [folder_id],
        }

        if not update_existing:

            # 3. Create an empty file to receive the exported content
            new_file = (
                service.files()
                .create(body=file_metadata, fields="id", supportsAllDrives=True)
                .execute()
            )
            new_file_id = new_file.get("id")
            # print(f"File ID: {new_file_id}")

        else:
            new_file_id = update_existing

        # 4. Download the exported content into the new file
        fh = io.BytesIO()  # Create an in-memory file-like object to store the download
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            done = downloader.next_chunk()

        # 5. Upload downloaded content to the new file
        fh.seek(0)  # Reset the file pointer to the beginning
        media_body = MediaIoBaseUpload(
            fh, mimetype=mime_type, resumable=True
        )  # Create MediaIoBaseUpload object
        service.files().update(
            fileId=new_file_id, media_body=media_body, supportsAllDrives=True
        ).execute()
        print(f"File updated: {export_path}")
        return new_file_id

    except HttpError as error:
        print(f"An error occurred in export_file - Retrying: {error}")
        export_file(
            service,
            file_id,
            mime_type,
            export_path,
            folder_id,
            update_existing,
            count + 1,
        )
