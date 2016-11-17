import requests

def getJobs():
    url = "http://imapex-chronic-bus.green.browndogtech.com/api/get"

    #response = requests.request("GET", url)

    #jobs = response.json()

    #for job in jobs:
    #    job['link'] = url + job
    #    job['status'] = "Complete"

    jobs = [{"job":"job", "link":"link", "status":"complete"}, {"job":"job","link":"link", "status":"complete"}, {"job":"job","link":"link", "status":"complete"}]
    return jobs