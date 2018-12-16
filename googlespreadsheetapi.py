from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.client import OAuth2WebServerFlow
import datetime, sys, copy, os
from path import Path
from dotenv import load_dotenv



## Where to find local env settings
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=False)


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
CELLS_RANGE = 'A1:C500'
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

def load_data_from_google_spreadsheet():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                           client_secret=CLIENT_SECRET,
                           scope=SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', '')

    ranges = [sheet['properties']['title']+"!"+CELLS_RANGE for sheet in sheets]

    all_data = []
    all_users = []

    for i, sheetinstance in enumerate(sheets):
        all_data.append({ "title": sheetinstance['properties']["title"], "rtl": sheetinstance['properties']['rightToLeft']})

    request = service.spreadsheets().values().batchGet(spreadsheetId = SPREADSHEET_ID, ranges = ranges)
    data = request.execute()
    values = data['valueRanges']

    for i, sheetinstance in enumerate(sheets):
        rows = values[i]['values']

        if rows[0] != ["user","image_url","status"]:
            print(f'No data found on {sheetinstance["properties"]["title"]}.')

        else:
            conversation_data = []
            sides = {}                     # initiate dictionary for user names and profile image

            for counter, row in enumerate(rows):
                if counter == 1:
                    try:
                        talker = { 'username': row[0], 'image_url': row[1], 'status':row[2]}
                        if row[0] not in all_users:
                            all_users+=[{'username': row[0], 'image_url': row[1], 'status':row[2]}]

                    except Exception as e:
                        print(row)
                        print(i)
                        print(sys.stderr, f"could  not find valid user1 details in row no. 2 of the spreadsheet")
                        print(e)
                        sys.exit(1)
                elif counter == 2:
                    try:
                        chatmate = { 'username': row[0], 'image_url': row[1], 'status':row[2]}
                        if row[0] not in all_users:
                            all_users+=[{'username': row[0], 'image_url': row[1], 'status':row[2]}]

                    except Exception as e:
                        print(sys.stderr, f"could not find valid user2 details in row no. 3 of the spreadsheet")
                        print(e)
                        sys.exit(1)

                elif counter > 3:

                    try:
                        time = datetime.datetime.strptime(str(row[2]),"%H:%M")
                    except Exception as e:
                        print (sys.stderr, f"illegal time was given on row[{counter}]: {row}")
                        print(e)
                        sys.exit(1)

                    if row[0] in [talker["username"], chatmate["username"]]:
                        user = row[0]
                    else:
                        print(row[0]+" was entered as a username, but is not included in the users list")
                        print(row)
                        print("talker: ", talker)
                        print("chatmate: ", chatmate)
                        sys.exit(1)

                    if not(row[1] == ''):
                        message = row[1]
                    else:
                        print(f"Illegal empty message string appears on {time}")
                        sys.exit(1)


                    conversation_data.append({"user":user, "message":message, "time": time})

            all_data[i]["thread"] = conversation_data
            all_data[i]["sides"] = {"talker": talker, "chatmate":chatmate}
            all_data[i]["talker"] = talker
            all_data[i]["chatmate"] = chatmate

    for i in range(0, len(all_data)):
        if "talker" in all_data[i] and "chatmate" in all_data[i]:
            all_data[i]["other_users"] = [user for user in all_users if (user["username"] != all_data[i]["talker"]["username"] and user["username"] != all_data[i]["chatmate"]["username"])]

    return(all_data)
