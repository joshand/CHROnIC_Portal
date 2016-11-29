import socket

from flask import render_template, redirect, request
from .forms import hcHealthAuthForm
from CHROnIC_Portal import app
from .tasks import getJobs, getReports, buildReportData
import json
import requests
import os
import pprint
import base64
busbaseurl = os.environ['CHRONICBUS']
ucsbaseurl = os.environ['CHRONICUCS']
mybaseurl = os.environ['CHRONICPORTAL']

@app.route("/")
def index():
    return render_template("index.html")
    #return redirect("/hc_auth", code=302)

@app.route("/hc_auth")
def hcAuth():
    form = hcHealthAuthForm()
    hostname = socket.gethostname()
    return render_template('ucshc_auth.html', form=form, hostname=hostname)

@app.route("/hc_status", methods=['POST'])
def hcStatus():
    ucs_hostname = request.form['ucs_hostname']
    ucs_username = request.form['ucs_username']
    ucs_password = request.form['ucs_password']
    vc_hostname = request.form['vc_hostname']
    vc_username = request.form['vc_username']
    vc_password = request.form['vc_password']
    channelid = request.form['channelid']

    url = busbaseurl + "/api/send/{}".format(channelid)
    headers = {'Content-type':'application/json'}

    with open('CHROnIC_Portal/ucs.json', 'r') as ucs_template:
        ucs = ucs_template.read()

    ucs = ucs.replace('%ip%', ucs_hostname)
    ucs = ucs.replace('%un%', ucs_username)
    ucs = ucs.replace('%pw%', ucs_password)

    #ucs = ucs.replace('\\\"', '\"')
    #ucs = ucs.replace('\"', '\\\"')

    content = '{"msgdata":"' + base64.b64encode(bytes(ucs, "utf-8")).decode("ascii") + '", "status": "0", "desc":"ucs"}'
    r = requests.post(url, data=content, headers=headers)
    print(url)
    print(r)
    print(content)

    with open('CHROnIC_Portal/vcenter.json','r') as vcenter_template:
        vcenter = vcenter_template.read()

    vcenter = vcenter.replace('%ip%', vc_hostname)
    vcenter = vcenter.replace('%un%', vc_username)
    vcenter = vcenter.replace('%pw%', vc_password)

    #vcenter = vcenter.replace('\\\"', '\"')
    #vcenter = vcenter.replace('\"', '\\\"')

    webhookurl = ucsbaseurl + "/api/{}".format(channelid)

    content = '{"msgdata":"' + base64.b64encode(bytes(vcenter, "utf-8")).decode("ascii") + '", "status": "0", "desc":"vcenter", "webhook":"' + webhookurl + '"}'
    r = requests.post(url, data=content, headers=headers)
    print(url)
    print(r)
    print(content)


    return redirect(mybaseurl + "/jobs", code=302)


@app.route("/jobs")
def jobs():
    jobs = getJobs()
    reports = getReports()
    hostname = socket.gethostname()
    return render_template('jobs.html', data=jobs, reports=reports, hostname=hostname)


@app.route("/report/<reportid>")
def report(reportid):
    #print(reportid)
    servers = buildReportData(reportid)
    hostname = socket.gethostname()

    return render_template('report.html', servers=servers, hostname=hostname)
