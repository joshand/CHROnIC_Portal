import socket

from flask import render_template, redirect, request
from .forms import hcHealthAuthForm
from CHROnIC_Portal import app
from .tasks import getJobs, getReports, buildReportData

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
    return "Credentials Accepted.  Sending to Josh's app"


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