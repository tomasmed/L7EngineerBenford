from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import pandas as pd

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

#Sqlite3 since the whole idea of the app is pretty light
DATABASE = '/sqlite/db'

@app.route("/")
def home():
    return "Hello, Flask!"

# Get the uploaded files
@app.route("/Task", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        # save the file
        parseCSV(file_path)

    return redirect(url_for('index'))
      
@ app.route("/Task")
def Task():
    return render_template(
        "base.html"

    )

def parseCSV(filePath):
      # CVS Column Names
      col_names = ['first_name','last_name','address', 'street', 'state' , 'zip']
      # Use Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      # Loop through the Rows
      for i,row in csvData.iterrows():
            print(i,row['first_name'],row['last_name'],row['address'],row['street'],row['state'],row['zip'],)

