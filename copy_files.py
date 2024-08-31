"""
This module contains functions for interacting with Google Sheets and Google Drive APIs.
"""

import socket
from constants import SCHOOLS, QUERIES, FILE_FORMATS
from create_service import create_service
from sheet_functions import (
    get_sheets,
    get_ss_name,
    read_sheet,
    update_sheet,
    copy_spreadsheet,
)
from drive_functions import find_file, export_file

socket.setdefaulttimeout(600)
sheets_service = create_service("sheets", "v4")
drive_service = create_service("drive", "v3")


def main():
    """
    This function builds the necessary service objects to interact with Google Sheets and Google
    Drive APIs.
    It iterates over a list of schools and performs the following actions:
    1. Retrieves the spreadsheet ID and name for each school.
    2. Retrieves the folders associated with each school.
    3. Retrieves the sheets associated with each spreadsheet.
    4. For each folder, it iterates over a list of file formats.
    5. If the file format is a sheet, it checks if a file with the spreadsheet name already
    exists in the folder.
       If it does, it retrieves the values from the corresponding sheet and updates the sheet in the
       destination file.
       If it doesn't, it copies the spreadsheet to the folder.
    6. If the file format is an XLSX file, it checks if a file with the spreadsheet name and XLSX
    extension already exists in the folder.
       If it does, it exports the spreadsheet to the destination file.
       If it doesn't, it exports the spreadsheet to the folder.
    7. If the file format is a PDF file, it iterates over the sheets associated with the
    spreadsheet.
       For each sheet, it checks if a file with the spreadsheet name, sheet name, and PDF extension
       already exists in the folder.
       If it does, it exports the sheet to the destination file.
       If it doesn't, it exports the sheet to the folder.
    """
    # Build the service objects
    for school in SCHOOLS:
        # print(school.get("schoolid"))
        ssid = school.get("ssid")
        ss_name = get_ss_name(sheets_service, ssid)
        # print(ss_name)
        folders = school.get("folders")
        sheets = get_sheets(sheets_service, ssid)
        for folder in folders:
            for file_format in FILE_FORMATS:
                # if sheet then save name
                if file_format.get("name") == "sheet":
                    file_name = ss_name
                    existing_file = find_file(drive_service, file_name, folder)
                    if existing_file:
                        destination_file_id = existing_file.get("id")
                        for sheet in sheets.get("sheets"):
                            sheet_name = sheet.get("properties").get("title")
                            values = read_sheet(ssid, sheet_name, sheets_service)
                            columns = {
                                query.get("sheetName"): query.get("columns")
                                for query in QUERIES
                            }.get(sheet_name)
                            update_sheet(
                                sheets_service,
                                destination_file_id,
                                sheet_name,
                                values,
                                columns,
                                True,
                            )
                    else:
                        copy_spreadsheet(ssid, ss_name, drive_service, folder)

                # if xlsx then save name with .xlsx
                elif file_format.get("name") == ".xlsx":
                    file_name = ss_name + file_format.get("name")
                    existing_file = find_file(drive_service, file_name, folder)
                    if existing_file:
                        export_file(
                            drive_service,
                            ssid,
                            file_format.get("mimeType"),
                            file_name,
                            folder,
                            existing_file.get("id"),
                        )
                    else:
                        export_file(
                            drive_service,
                            ssid,
                            file_format.get("mimeType"),
                            file_name,
                            folder,
                            None,
                        )

                # if pdf then save name with sheetname and .pdf
                elif file_format.get("name") == ".pdf":
                    if school.get("schoolid") == 0:
                        continue
                    for sheet in sheets.get("sheets"):
                        sheet_name = sheet.get("properties").get("title")
                        file_name = (
                            ss_name + " - " + sheet_name + file_format.get("name")
                        )
                        existing_file = find_file(drive_service, file_name, folder)
                        if existing_file:
                            export_file(
                                drive_service,
                                ssid,
                                file_format.get("mimeType"),
                                file_name,
                                folder,
                                existing_file.get("id"),
                            )
                        else:
                            export_file(
                                drive_service,
                                ssid,
                                file_format.get("mimeType"),
                                file_name,
                                folder,
                                None,
                            )


if __name__ == "__main__":
    main()
