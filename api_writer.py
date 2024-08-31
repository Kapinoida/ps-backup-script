"""
API Test.py
"""

import datetime
import json
import requests
from get_connection import get_connection
from constants import QUERIES, SCHOOLS
from create_service import create_service
from sheet_functions import update_sheet


sheet_service = create_service("sheets", "v4")


def get_current_year_id():
    """Return the current year ID."""
    today = datetime.date.today()
    if today.month <= 6:
        return today.year - 1991
    return today.year - 1990


def get_ps_api_data(school, year, connection, query):
    """
    Retrieves data from the PowerSchool API.

    This function establishes a connection to the PowerSchool API by calling the `get_connection`
    function.
    It then sends a POST request to the specified URL with the required headers and payload.
    The response from the API is returned.

    Returns:
        response: The response object containing the data retrieved from the PowerSchool API.
    """

    headers = {
        "Authorization": connection[1] + " " + connection[0],
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "schoolid": school,
        "yearid": year,
    }
    try:
        response = requests.post(
            query.get("url"), headers=headers, data=json.dumps(payload), timeout=10
        )
        return make_list(response.json().get("record"), query)
    except requests.exceptions.RequestException as error:
        print(f"An error occurred in get_ps_api_data: {error}")
        return None


def make_list(record, query):
    """
    Creates a list of data based on the input record.

    Parameters:
        record (list): The input record containing data.

    Returns:
        list: A list of processed data.
    """
    data = []
    if record is not None:
        for i in record:
            temp_row = []
            for col in query.get("columns"):
                temp_row.append(i.get("tables").get("students").get(col))
            data.append(temp_row)
    return data


def main():
    """
    This function retrieves school information using the PowerSchool API and updates
    the respective sheet.
    No parameters or return types specified.
    """
    connection = get_connection()
    for school in SCHOOLS:
        for query in QUERIES:
            school_info = get_ps_api_data(
                school.get("schoolid"), get_current_year_id(), connection, query
            )
            if school_info:
                update_sheet(
                    sheet_service,
                    school.get("ssid"),
                    query.get("sheetName"),
                    school_info,
                    query.get("columns"),
                    False,
                )


if __name__ == "__main__":
    main()
