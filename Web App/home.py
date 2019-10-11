from flask import Flask, render_template, flash, redirect, url_for, session, logging,request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import datetime
from dateutil.parser import parse
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
from tests import run_tests
from mail import send_mail
from algo import run

app = Flask(__name__)

class createForm(Form):
    par1 = StringField('Parameter 1', [validators.Length(min=1, max=1)])

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        par = str(request.form.get('par'))
        session['par'] = par
        return redirect(url_for('cityDetails'))
    return render_template('index.html')

@app.route('/city-details',methods=['GET','POST'])
def cityDetails():
    population_density = {'Janakpuri':14000, 'Mayapuri':14000, 'N.Y.':5500, 'Nizamuddin':70000, 'Pritampura':14000,
                         'Shahadra':59000, 'Shahzada':14000, 'Siri':8200}
    par = session.get('par')
    pp_density = population_density[(par.split('_')[0]).split()[0]]
    city_name = par.split('_')[0]+', Delhi'
    type_loc = par.split('_')[-1][0].upper() + par.split('_')[-1][1:]
    if request.method=='POST':
        predicts = run('city_data/'+par+'.csv')
        session['predicts'] = predicts
        aqi = []
        for i in predicts.values():
            aqi.append(i[2])
        session['max_aqi'] = max(aqi)
        session['min_aqi'] = min(aqi)
        if max(aqi)>=301:
            cur_date = str(datetime.date.today())
            file = open('last_sent_mail.txt','r+')
            d = file.readlines()
            file.seek(0)
            flag = 0
            for i in d:
                if str(parse(i).date())==cur_date:
                    flag=1
            if flag==0:
                send_mail('mycontacts.txt', 'govt_mail.txt', max(aqi))
                file.write(cur_date)
            else:
                pass
            file.truncate()

        return redirect(url_for('aqiTest'))
    return render_template('city-details.html', file_name = par.split('_')[0]+'.png', city_name=city_name, pp_density = pp_density, type_loc = type_loc)

@app.route('/city-details/aqi-test',methods=['GET','POST'])
def aqiTest():
    dc = session.get('predicts')
    max_aqi = session.get('max_aqi')
    min_aqi = session.get('min_aqi')

    if request.method=='POST':
        if request.form['share']=='Back to Home':
            return redirect(url_for('index'))
        else:
            return redirect(url_for('shareDetails'))

    return render_template('aqi-test.html', predicts = dc, min_aqi = min_aqi, max_aqi = max_aqi)

@app.route('/city-details/aqi-test/share-details',methods=['GET','POST'])
def shareDetails():
    if request.method=='POST':
        username = str(request.form.get('username'))
        email = str(request.form.get('email'))+','+str(request.form.get('email1'))
        subject = username + ' TO ' + str(request.form.get('subject'))

        contacts = [username, email.split(',')]
        send_mail(contacts, 'residential guidelines.txt', session.get('max_aqi'), subject)

        flash('Your message has been sent.')
        return redirect('/')

    return render_template('share-details.html')


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.secret_key = 'secret12'
    app.run('localhost', 1234, debug=True)
