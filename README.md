# ps-backup-script

## Introduction

This project aims to create some PowerSchool backup data to use in case of an outage. Data would be pulled every day and stored into multiple file types and shared drives for easier access.
There are two main scripts used in this project:

- api_writer.py
- copy_files.py

There is also a couple of helper python files that were built as well:
- constants.py - Holds some of the constants we use in the project.
- drive_functions.py - Holds functions that are used with the Google Drive service.
- sheet_functions.py - Hold functions that are used with the Google Sheets service.
- stess_test_runner.py - Can run a defined number of iterations of a script to help figure out if things run smoothly and pick out errors quicker before deploying.

## api-writer.py

This script uses the PowerSchool API to grab data from a PowerQuery and write that data to an appropriate Google Sheet.

### Requirements

- Keyring - a module that lets you set up variables for getting passwords or other sensitive information without directly adding it to the script. More information about setup below.
- Google Cloud Credentials - Need to have a project ready and the credentials JSON downloaded. More information below. (Possible to shift this into a service account?)

### Explanation

1. First, we establish a connection to the PowerSchool API by creating a new token.
2. Then we loop through each school and query to run and write to the appropriate spreadsheet and sheet.

## copy_files.py

This script uses Google APIS to copy a Google Sheet into different formats in different shared drives.

### Requirements

- Google Cloud Credentials - Need to have a project ready and the credentials JSON downloaded. More information below. (Possible to shift this into a service account?)

### Explanation

1. Loops through each school and gets some info from the Sheets.
2. Loops through each folder for that school.
3. Loops through each file format and looks if it exists.
   1. If it does, update that file.
   2. If not, create a new file.

## Keyring

We can use keyring to store sensitive data locally, and then get that stored data into variable for use in scripts. We want to use something like this so we can store information like passwords, API keys, and other important information behind a barrier.
[min201 Keyring Documentation](https://github.com/Minooka-CCSD-201/min201-documentation/blob/main/keyring.md)

## Google Cloud

Google Cloud is how we can interact with Google's API and mess with things like Sheets, Drive, and Gmail. The scripts that in production use a centralized account.
[min201 Google Cloud Console](https://github.com/Minooka-CCSD-201/min201-documentation/blob/main/google-cloud-console.md)
