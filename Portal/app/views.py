"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

#Import pyodbc module using below command
import pyodbc as db

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
 
    #Create connection string to connect EarlyYears database with windows authentication
    con = db.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=LT-SRV-MISADEV3;Trusted_Connection=no;DATABASE=EarlyYears;UID=RobinEY;PWD=RobinEY')
    # con = db.connect('DSN=ODBCSQLServer11;UID=RobinEY;PWD=RobinEY')
    cur = con.cursor()
 
    #SELECT all rows from LA table
    qry = 'SELECT LACode, LAName FROM EarlyYears.GIS.LA WHERE LACode = \'E09000012\''
    cur.execute(qry)
 
    row = cur.fetchone() #Fetch first row
    s = ''
    while row: #Fetch all rows using a while loop
        if s == '':
            s = row.LACode + '\t' + row.LAName
        else:
            s = s + '\n' + row.LACode + '\t' + row.LAName
        row = cur.fetchone()
    cur.close() #Close the cursor and connection objects
    con.close()    
    
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':s,
            'year':datetime.now().year,
        }
    )
