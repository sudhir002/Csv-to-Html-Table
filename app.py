from flask import Flask, request, render_template
import pandas as pd
import datetime
from pymongo import MongoClient

app = Flask(__name__)

def mongo_connect():
    client = MongoClient('localhost', 27017)
    return client.sententia


@app.route('/upload_file', methods=["POST"])
def upload_file():
    try:
        file = request.files["file"]
        type_of_file = file.filename.rsplit(".", 1)[1]
        if type_of_file == "json":
            df = pd.read_json(file)
        elif type_of_file == "csv":
            df = pd.read_csv(file)
        elif type_of_file == "xlsx":
            df = pd.read_excel(file)
        else:
            return ({"table_data": "wrong file type, only upload csv , excel, json with required structure"})

        #upload into db
        db = mongo_connect()
        db["user_file_data"].insert({"date": datetime.datetime.now(), "data": df.to_dict("records")})

        df.columns = list(df.columns)
        df = df.to_html()
        htmlpage_content = "<html><head></head><body style='text-align:center;'><div>{}</div></body></html>".format(str(df))
        return ({"table_data":htmlpage_content})
    except Exception as e:
        return ({"table_data":"something went wrong"})

if __name__ == '__main__':
    app.run()