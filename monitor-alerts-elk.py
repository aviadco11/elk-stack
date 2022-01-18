from datetime import datetime
from elasticsearch import Elasticsearch
import smtplib
import requests

from ssl import create_default_context

def Check_Valid_ELK():
    print("\nCheck Valid ELK\n")
    try:
        res = requests.get(url = 'https://elk6.westeurope.cloudapp.azure.com:9200', auth=('elastic','xune7bvbmFmmhAPjnrqA'), verify=False, timeout=4 )
        print(res.content)
        if res.status_code != 200:
            print("ConnectTimeout!")
            return False
    except Exception as e:
        print(e)
        return False
    return True


def Check_Health_ELK(es):
    print("\nCheck Health\n")
    print(es.cluster.health())
    res = es.cluster.health()

    return res['status']


def Check_Alerts_Idx_ELK(es):
    print("\nCheck Alerts\n")
    res = es.search(index="index", query={"match_all": {}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit["_source"])

print("Monitor Running : ", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

def SendEmail(email,password,from_address,to_address,msg):
    try:
        smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_object.starttls()
        smtp_object.login(email, password)
        smtp_object.sendmail(from_address, to_address, msg)
    except Exception as e:
        print(e)
        print("Mail Wasnt send\n")
        return False
    print("Mail Was send")
    return False


email = 'aviad.co1@gmail.com'
from_address = 'aviad.co1@gmail.com'
to_address = 'aviad.co1@gmail.com'
password = 'mnnonvbgyoadqyhy'

if Check_Valid_ELK():
        context = create_default_context(cafile=""c:/certs/elasticsearch-ca.pem"")
        es = Elasticsearch(
        ['elk6.westeurope.cloudapp.azure.com'],
        http_auth=('elastic', 'xune7bvbmFmmhAPjnrqA'),
        #api_key='VWdGUEtuNEJSeTdWZnFtcUVlcVo6eVpZOTM1QzFRMjZHVU9GVmlxdlhSQQ',
        scheme="https",
        port=9200,
        ssl_context=context,
        )
        if Check_Health_ELK(es) != 'green':
            subject = "ElasticSearch Not Healthy - Critical Alert !!!"
            message = "ElasticSearch Status is not Healthy"
            msg = "Subject: " + subject + '\n' + message
            SendEmail(email, password, from_address, to_address, msg)
            print(msg)
        Check_Alerts_Idx_ELK(es)
else:
    subject = "ElasticSearch Validation - Critical Alert !!!"
    message = "ElasticSearch is Down"
    msg = "Subject: "+subject+'\n'+message
    SendEmail(email,password,from_address,to_address,msg)
    print(msg)
