from turtle import update, width
from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import pandas as pd
import altair as alt

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
@app.route("/Task", methods=['GET','POST'])
def uploadFiles():
    # get the uploaded file
    

    if request.method == 'POST':
        #uploaded_file = pd.read_csv(request.files['file'], sep = '\t')
        df = pd.read_csv(request.files['file'], sep = '\t')
        colname = request.form['colname']
        #chosen_col = '7_2009'
        #uploaded_file['Leading Digit'] = uploaded_file[chosen_col].astype(str).str[0]

        Benford_dist = pd.DataFrame({ 'Leading Digit': [1,2,3,4,5,6,7,8,9] , 'Percentage' : [30.1,17.6,12.5,9.7,7.9,6.7,5.8,5.1,4.6]})

        chosen_col = colname
        df['Leading Digit'] = df[chosen_col].astype(str).str[0]

        #Create a dataframe with the "Benford Distribution of The target column"
        ##Altair Graphing
        
        sfg = pd.DataFrame({'Count' : df.groupby( [ 'Leading Digit'] ).size()}).reset_index()

        benDist = alt.Chart(Benford_dist).mark_line(color="orange").encode(
                    x = alt.X("Leading Digit:N"),
                    y= "Percentage:Q",
                )

        sfg = sfg[ sfg['Leading Digit'] != '0']
        chart = alt.Chart(sfg).transform_joinaggregate(
            TotalCount= 'sum(Count)',
        ).transform_calculate(
            Percentage = "datum.Count*100.0 / datum.TotalCount" 
        ).mark_bar().encode(
                    x = alt.X("Leading Digit:N"),
                    y= "Percentage:Q",
                )
        chart = (chart + benDist).resolve_scale(x="shared").properties(title="Benford's Distribution vs " + chosen_col, width= 800, height = 800 )

        
        sfg['Percent'] = sfg['Count'] *100  / sum(sfg['Count'])
        df_p = sfg[sfg['Leading Digit'] == '1']
        BenfordCheck = df_p['Percent']
        chart.save('test2.html')

        return render_template('base2.html',shape= sfg.shape, assertion = BenfordCheck.to_json(), graph = chart.to_json() ,colname=chosen_col)

    return  render_template('base.html')


@app.route("/Task/test", methods=['GET','POST'])
def Task():
    if request.method == 'POST':
        #uploaded_file = pd.read_csv(request.files['file'], sep = '\t')
        df = pd.read_csv(request.files['file'], sep = '\t')

        return render_template("col_pick.html",cols = df.columns)

    return render_template("base.html")



def parseCSV(filePath):
      # CVS Column Names
      col_names = ['first_name','last_name','address', 'street', 'state' , 'zip']
      # Use Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      # Loop through the Rows
      for i,row in csvData.iterrows():
            print(i,row['first_name'],row['last_name'],row['address'],row['street'],row['state'],row['zip'],)

