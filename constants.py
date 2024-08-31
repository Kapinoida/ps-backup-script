"""
This module contains constants used in the PowerSchool API interaction.
It includes a list of queries, schools, and file formats.
"""

AUTH_URL = "https://min201.powerschool.com/oauth/access_token"

QUERIES = [
    {
        "sheetName": "Transportation Info",
        "url": "https://min201.powerschool.com/ws/schema/query/org.d201.students.transport_info_per_building?pagesize=0",
        "columns": [
            "student_number",
            "lastfirst",
            "grade_level",
            "team",
            "street",
            "transportation_mode_before",
            "pickup_bus",
            "pickup_time",
            "pickup_location",
            "daycare_before",
            "daycare_before_name",
            "daycare_before_address",
            "daycare_before_phone",
            "transportation_mode_after",
            "dropoff_bus",
            "dropoff_time",
            "dropoff_location",
            "daycare_after",
            "daycare_after_name",
            "daycare_after_address",
            "daycare_after_phone",
            "daycare_arrangements",
        ],
    },
    {
        "sheetName": "Schedule Info",
        "url": "https://min201.powerschool.com/ws/schema/query/org.d201.students.student_schedule_per_building?pagesize=0",
        "columns": [
            "student_number",
            "lastfirst",
            "grade_level",
            "teacher",
            "course_name",
            "ee",
            "room",
            "period_number",
            "time",
        ],
    },
    {
        "sheetName": "Contact Info",
        "url": "https://min201.powerschool.com/ws/schema/query/org.d201.students.student_contacts_per_building?pagesize=0",
        "columns": [
            "student_number",
            "lastfirst",
            "grade_level",
            "home_room",
            "primary",
            "custodial",
            "emergency",
            "contname",
            "contrel",
            "contphone",
            "contemail",
        ],
    },
]

ALLBACKUPSID = "0AGF1TXP-FyyIUk9PVA"

SCHOOLS = [
    {
        "schoolid": 0,
        "ssid": "1ee5iC3n__THFqEpcTHoNhtk56RJyHa6Uu_5RpvGOG5M",
        "folders": [ALLBACKUPSID],
    },
    {
        "schoolid": 1150,
        "ssid": "1Ex9o1_SEJBdVTA2MZjGSU8pUn95CRRGal8Y1_amjUyE",
        "folders": [ALLBACKUPSID, "0AGvZHAEWASsyUk9PVA"],
    },
    {
        "schoolid": 5177,
        "ssid": "19ecfAWUH4qRIgmqyJQZHaog-E4JFT66VzhP07g3DDVY",
        "folders": [ALLBACKUPSID, "0APxtexiQIwCvUk9PVA"],
    },
    {
        "schoolid": 5197,
        "ssid": "1t2Tr8DhwT3UVVcxC9SMbbGTcoAuj14yltVeQl5YGPTA",
        "folders": [ALLBACKUPSID, "0AKwEIKLRyIhQUk9PVA"],
    },
    {
        "schoolid": 11095,
        "ssid": "1a9F2-oo4QwlOsllCt-zdMRFxJ4KJ0O-1Bh4gwC3dXcc",
        "folders": [ALLBACKUPSID, "0AJvNRqaC8G49Uk9PVA"],
    },
    {
        "schoolid": 17906,
        "ssid": "1rT4lPQEtFE3smXv5hLU_RM_hKzFnseQ0ItVkIUfREzc",
        "folders": [ALLBACKUPSID, "0APlIK2ERAsrVUk9PVA"],
    },
    {
        "schoolid": 31622,
        "ssid": "1OzTPf_e5370JL9Kwk310XaQL1JL4WFdxhON8n-Ohdb4",
        "folders": [ALLBACKUPSID, "0AHlNfafsdbhpUk9PVA"],
    },
    {
        "schoolid": 31948,
        "ssid": "1yXcf4GOcybYMjnAyqZUN8Zp7SScP0VrG4p6_XQcP12s",
        "folders": [ALLBACKUPSID, "0AIRdMtwEJQB7Uk9PVA"],
    },
]

FILE_FORMATS = [
    {
        "mimeType": "sheet",
        "name": "sheet",
    },
    {
        "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "name": ".xlsx",
    },
    {
        "mimeType": "application/pdf",
        "name": ".pdf",
    },
]
