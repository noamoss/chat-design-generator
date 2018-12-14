from flask import Flask, render_template, request, session, flash, redirect, url_for
from googlespreadsheetapi import  load_data_from_google_spreadsheet
from chatboxes import messagetemplate
import datetime
from dotenv import load_dotenv
from os import environ

is_prod = environ.get('IS_HEROKU', None)


app = Flask(__name__)

if is_prod == "TRUE":
    app.config['DEBUG'] = environ.get('DEBUG')

else:
    app.config.from_pyfile('.env')


@app.route('/<int:sheet_id>',methods=['GET'])
def show_chat(sheet_id=0):
    messages = []
    all_data = load_data_from_google_spreadsheet()

    for message_info in all_data[sheet_id]["thread"]:
        messages.append(messagetemplate(username=message_info["user"], message=message_info["message"],time=datetime.datetime.strftime(message_info["time"],"%H:%M"), sides = (all_data[sheet_id]["talker"],all_data[sheet_id]["chatmate"])))
    all_data[sheet_id]["messages"] = messages

    return render_template('basic_template.html', data = all_data[sheet_id])

if __name__ == "__main__":
    app.run()
