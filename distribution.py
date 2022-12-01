import secrets
import pandas as pd
import requests
import logging
import time

def create_Distribution(apiToken, dataCenter, libraryId, messageId, mailingListId, fromEmail, replyToEmail, fromName,
                        subject, surveyId, expirationDate, sendDate):
    # Static Params
    baseUrl = "https://{0}.qualtrics.com/API/v3/distributions".format(dataCenter)
    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
    }

    # Payload
    payload = {
        "message": {
            "libraryId": "{0}".format(libraryId),
            "messageId": "{0}".format(messageId),
        },
        "recipients": {
            "mailingListId": "{0}".format(mailingListId),
        },
        "header": {
            "fromEmail": "{0}".format(fromEmail),
            "replyToEmail": "{0}".format(replyToEmail),
            "fromName": "{0}".format(fromName),
            "subject": "{0}".format(subject),
        },
        "surveyLink": {
            "surveyId": "{0}".format(surveyId),
            "expirationDate": "{0}".format(expirationDate),
            "type": "Individual"
        },
        "sendDate": "{0}".format(sendDate)
    }

    # Send it
    response = None
    while response is None:
        try:
            response = requests.request("POST", baseUrl, json=payload, headers=headers)
            if response.json()["meta"]["httpStatus"] == "200 - OK":
                response = response
            else:
                response = None
                time.sleep(60)
        except:
            time.sleep(60)

    print(response)
    logging.info(response.json())
    return response.json()["result"]["id"]


def create_Reminder(apiToken, dataCenter, libraryId, messageId, distributionId, fromEmail, replyToEmail, fromName,
                    subject, sendDate):
    # Static Params
    baseUrl = "https://{0}.qualtrics.com/API/v3/distributions/{1}/reminders".format(dataCenter, distributionId)
    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
    }

    payload = {
        "message": {
            "libraryId": "{0}".format(libraryId),
            "messageId": "{0}".format(messageId),
        },
        "header": {
            "fromEmail": "{0}".format(fromEmail),
            "replyToEmail": "{0}".format(replyToEmail),
            "fromName": "{0}".format(fromName),
            "subject": "{0}".format(subject),
        },
        "sendDate": "{0}".format(sendDate)
    }

    response = requests.request("POST", baseUrl, json=payload, headers=headers)

    logging.info(response.text)
    return response.json()["result"]["distributionId"]


def create_ThankYou(apiToken, dataCenter, libraryId, messageId, distributionId, fromEmail, replyToEmail, fromName,
                    subject, sendDate):
    # Static Params
    baseUrl = "https://{0}.qualtrics.com/API/v3/distributions/{1}/thankyous".format(dataCenter, distributionId)
    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
    }

    payload = {
        "message": {
            "libraryId": "{0}".format(libraryId),
            "messageId": "{0}".format(messageId),
        },
        "header": {
            "fromEmail": "{0}".format(fromEmail),
            "replyToEmail": "{0}".format(replyToEmail),
            "fromName": "{0}".format(fromName),
            "subject": "{0}".format(subject),
        },
        "sendDate": "{0}".format(sendDate)
    }

    response = requests.request("POST", baseUrl, json=payload, headers=headers)

    logging.info(response.text)
    return response.json()["result"]["distributionId"]


def get_contacts_from_sample(apiToken, dataCenter, directoryId, sampleId):

    baseUrl = "https://{0}.qualtrics.com/API/v3/directories/{1}/samples/{2}/contacts".format(dataCenter, directoryId, sampleId)

    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
    }

    response = requests.request("GET", baseUrl, headers=headers)
    print(response)
    contactstuff = []
    while response.json()['result']['nextPage'] is not None:
        for elems in response.json()['result']['elements']:
            contactstuff.append(elems)

        response = requests.request("GET", response.json()['result']['nextPage'], headers=headers)

    for elems in response.json()['result']['elements']:
        contactstuff.append(elems)

    return contactstuff


def update_contact(apiToken, dataCenter, directoryId, contactId, banditgroup):

    url = "https://{0}.qualtrics.com/API/v3/directories/{1}/contacts/{2}".format(dataCenter, directoryId, contactId)

    payload = {
        "embeddedData": {'banditgroup': banditgroup},
    }
    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": apiToken
    }

    response = requests.request("PUT", url, json=payload, headers=headers)

    logging.info(response.text)
    print(response.text)
    return response.json()['meta']['httpStatus']

def create_sample(apiToken, dataCenter, directoryId, sampledefinitionId, previoussampleId):

    url = "https://{0}.qualtrics.com/API/v3/directories/{1}/samples".format(dataCenter, directoryId)

    payload = {
        "sampleDefinitionId": sampledefinitionId,
        "parentId": previoussampleId,
    }
    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": apiToken
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    logging.info(response.text)
    return response.json()['result']['sampleId']



def create_sample_definition(apiToken, dataCenter, directoryId, banditgroup):

    url = "https://{0}.qualtrics.com/API/v3/directories/{1}/samples/definitions".format(dataCenter, directoryId)

    payload = {
  "sampleCriteria": {
    "simpleFilter": {
      "filterType": "embeddedData",
      "comparison": "eq",
        "field": "banditgroup",
      "value": banditgroup
    }
  },
        "maxSampleSize": 1400,
        "samplePercentage": 0
}
    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": apiToken
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    logging.info(response.text)
    return response.json()['result']['sampleDefinitionId']



def get_directory_contact_history(apiToken, dataCenter, directoryId, contactId):

    url = "https://{0}.qualtrics.com/API/v3/directories/{1}/contacts/{2}/history".format(dataCenter, directoryId, contactId)

    querystring = {"type":"email"}

    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": apiToken
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()['result']['elements']



def delete_distribution(apiToken, dataCenter, distributionId):
    url = "https://{0}.qualtrics.com/API/v3/distributions/{1}".format(dataCenter, distributionId)

    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": apiToken
    }

    response = requests.request("DELETE", url, headers=headers)

    print(response.text)



def get_contact(dataCenter, directoryId, contactId, apiToken):


    url = "https://{0}.qualtrics.com/API/v3/directories/{1}/contacts/{2}".format(dataCenter, directoryId, contactId)

    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": apiToken
    }

    response = requests.request("GET", url, headers=headers)

    #print(response.text)
    return response.json()['result']['embeddedData']['bvdid']
