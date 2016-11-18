import requests
import pprint
import ast

def getReports():
    url = "http://imapex-chronic-bus.green.browndogtech.com/api/get"
    response = requests.request("GET", url)
    channels = response.json()

    reports = []
    for channel in channels:
        if "report" in channel:
            channels[channel]['status'] = "complete"
            reports.append({'report': channel, 'link': '/report/{}'.format(channel), 'status': channels[channel]['status']})

    return reports



def getJobs():
    url = "http://imapex-chronic-bus.green.browndogtech.com/api/get"
    response = requests.request("GET", url)
    channels = response.json()
    jobs = []

    basebuildlink = "http://imapex-chronic-ucs-esx-analyzer.green.browndogtech.com/api/"

    for channel in channels:
        if "report" not in channel:
            tracker = 0
            for task in channels[channel].keys():
                if channels[channel][task] != "2":
                    tracker = tracker + 1
            if tracker == 0:
                channels[channel]['status'] = "complete"
            else:
                channels[channel]['status'] = "in progress"
            jobs.append({'job':channel, 'link':basebuildlink + channel, 'status':channels[channel]['status']})

    pprint.pprint(channels)
    pprint.pprint(jobs)
    return jobs

def buildReportData(reportid):
    url = "http://imapex-chronic-bus.green.browndogtech.com/api/get/{}/2".format(reportid)
    response = requests.request("GET", url)

    data = response.json()

    servers = ast.literal_eval(data[0]['msgdata'])
    formated_servers = []
    for server in servers:
        fserver = {}
        print(server)
        fserver['location'] = server['ucs']['@dn'][0]
        fserver['type'] = server['ucs']['@model'][0]
        fserver['serial'] = server['ucs']['@serial'][0]
        fserver['os'] = "ESX " + server['esx']['version/~'][0]
        fserver['firmware'] = server['ucs']['mgmtController/firmwareRunning/@version'][1]
        fserver['firmware_support'] = server['firmware_status']
        fserver['enic_status'] = server['enic_status']
        fserver['supported_enic'] = server['supported_enic']
        fserver['running_enic'] = (server['esx']['driverinfo']['3']).split()[-1]
        fserver['fnic_status'] = server['fnic_status']
        fserver['supported_fnic'] = server['supported_fnic']
        fnic_long = (server['esx']['driverinfo']['1']).split()[2]
        fserver['running_fnic'] = fnic_long.split("-")[0]

        formated_servers.append(fserver)

    pprint.pprint(formated_servers)
    return formated_servers