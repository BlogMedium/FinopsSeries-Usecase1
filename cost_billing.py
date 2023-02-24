import datetime
import boto3
import json
from string import Template
import sys
import csv
from csv import DictReader
import operator
import logging
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta
import seaborn as sns



def  Message_teams(results, fetchdata, url):
    msg = pymsteams.connectorcard("https://outlook.office.com/webhook/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    msg.title(fetchdata)
    df = pd.read_csv(results)
    data = pd.DataFrame(df)
    print(data.to_html())
    msg.text(data.to_html())
    print(len(url))
    print("url0",url[0])
    print("url1",url[1])
    print("url2",url[2])
    print("url3",url[3])
    print("url4",url(4))
    msg.addLinkButton("For Monthly Cost Graph", url[0])
    msg.addLinkButton("Top 5 Region Usage for last 6 months", url[1])
    msg.addLinkButton("Top 5 Service Usage for last 6 months", url[3])
    msg.addLinkButton("Top 3 Region graph", url[4])
    msg.addLinkButton("Top 3 Service graph", url[5])
    msg.send()

def FindMonths(d,x):
    newmonth = ((( d.month - 1) + x ) % 12 ) + 1
    newyear  = int(d.year + ((( d.month - 1) + x ) / 12 ))
    return datetime.date( newyear, newmonth, d.day)

def Generate_Cost_Csv(start_date, end_date):
    now = datetime.datetime.utcnow()
    start = datetime.date.strftime(start_date, '%Y-%m-%d')
    end = datetime.date.strftime(end_date, '%Y-%m-%d')
    profiles = ["dev", "test", "preprod", "prod"]
    flag=0
    for profile in profiles:
        print(profile)
        session = boto3.Session(profile_name=profile)
        cd = session.client('ce')

        results = []

        token = None
        while True:
            if token:
                kwargs = {'NextPageToken': token}
            else:
                kwargs = {}
            data = cd.get_cost_and_usage(TimePeriod={'Start': start, 'End': end}, Granularity='MONTHLY',
                                         Metrics=['UnblendedCost'], GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}],
                                         **kwargs)
            results += data['ResultsByTime']
            token = data.get('NextPageToken')
            if not token:
                break

        mm = now.strftime("%B")
        filename = mm + '.csv'
        print(filename)
        timecolarr = []
        amountcolarr = []
        print(type(timecolarr))
        if len(timecolarr) == 0:
            print("timecolarr is empty")
            with open(filename, 'a') as f:
                for result_by_time in results:
                    for group in result_by_time['Groups']:
                        timecol = result_by_time['TimePeriod']['Start']
                        objDate = datetime.datetime.strptime(timecol, '%Y-%m-%d')
                        final_timecol = datetime.datetime.strftime(objDate, '%Y %b')
                        timecolarr.append(final_timecol)
                        amount = group['Metrics']['UnblendedCost']['Amount'].split(".")[0]
                        amountcolarr.append(amount)
                accountinfo = str((group['Keys']))[1:-1].replace("'", "")
                timecolarrstr = str(timecolarr)[1:-1].replace("'", "").strip()
                print(accountinfo)
                restimeamo = str(amountcolarr)[1:-1].replace("'", "").strip()
                print(restimeamo)
                if flag == 0:
                    print(','.join(['Account', timecolarrstr]), file=f)
                    flag = flag + 1
                if flag == 1:
                    print(','.join([accountinfo, restimeamo]), file=f)
    wordstartDate = start_date.strftime("%B %Y")
    costendDate = end_date.replace(day=1) - datetime.timedelta(1)
    wordendDate = costendDate.strftime("%B %Y")
    print(wordendDate)
    print(wordstartDate)
    fetchdata = " AWS Billing Report for the month" + " " + wordstartDate + " " + "to" + " " + wordendDate
    print(fetchdata)
    return (f.name, fetchdata)

def Generate_Cost_Service_Region(start_date_month, end_date, costtype):
    now = datetime.datetime.utcnow()
    start_month = datetime.date.strftime(start_date_month, '%Y-%m-%d')
    print("The start date is", start_month)
    end_month = datetime.date.strftime(end_date, '%Y-%m-%d')
    print("The end date is", end_month)
    year, month, day = map(int, start_month.split('-'))
    start_month_cal = datetime.date(year, month, day)
    year, month, day = map(int, end_month.split('-'))
    end_month_cal = datetime.date(year, month, day)
    num_months = (end_month_cal.year - start_month_cal.year) * 12 + (end_month_cal.month - start_month_cal.month)
    mm = now.strftime("%B")
    if num_months < 2:
        filename = mm + costtype + 'monthly' + '.csv'
    else:
        filename = mm + costtype  + '.csv'

    print("This is the filename for monthly region and service csv", filename)
    with open(filename, 'a') as f:
        print(','.join(['TimePeriod', 'LinkedAccount', costtype, 'Amount']), file=f)
        f.close()
        # Modify the Profile name here. Provide the name for the account which is provided in profile
        profiles = ["dev", "test", "prod"]
        for profile in profiles:
            print(profile)
            session = boto3.Session(profile_name=profile)
            cd = session.client('ce')

            results = []

            token = None
            while True:
                if token:
                    kwargs = {'NextPageToken': token}
                else:
                    kwargs = {}
                data = cd.get_cost_and_usage(TimePeriod={'Start': start_month, 'End': end_month}, Granularity='MONTHLY',
                                             Metrics=['UnblendedCost'],
                                             GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                                                      {'Type': 'DIMENSION', 'Key': costtype }],
                                             **kwargs)
                results += data['ResultsByTime']
                token = data.get('NextPageToken')
                if not token:
                    break
            with open(filename, 'a') as f:
                for result_by_time in results:
                    for group in result_by_time['Groups']:
                        timecol = result_by_time['TimePeriod']['Start']
                        accountname = ",".join(map(str, group['Keys']))
                        print(accountname)
                        amount = group['Metrics']['UnblendedCost']['Amount']
                        fetchdata = [timecol, accountname, amount]
                        print(",".join(map(str, fetchdata)), file=f)
        print("This is first irteration")
        return(filename)


def generate_bar_charts(results, fetchdata):
    data = pd.read_csv(results, encoding='utf-8')
    account = data['Account']
    data = data.drop(columns="Account")
    df = pd.read_csv(results, header=0, sep=',')

    # set width of bar
    barWidth = 0.1
    plt.figure(figsize=(20, 3))
    # Set position of bar on X axis
    x_pos = np.arange(len(data.columns))

    # Loop through each row of the data frame
    for i, row in data.iterrows():
        plt.bar(x_pos + i * barWidth, row.values, color=['black', 'green', 'blue', 'orange'][i % 4], 
                width=barWidth, edgecolor='white', label=account[i])

    # Add xticks on the middle of the group bars
    plt.xticks(x_pos + (len(data) - 1) / 2 * barWidth, data.columns)

    # Create legend & Show graphic
    plt.ylabel("AWS COST($)")
    plt.legend()
    plt.title(fetchdata)
    x = results.split(".")
    picturename = x[0] + ".png"
    plt.savefig(picturename)
    plt.show()
    return picturename

def upload_barchart(picturename):
    session = boto3.Session(profile_name='rnd')
    s3 = session.resource('s3')
    s3.Object('billing-dashboard', picturename).upload_file(Filename='C:\\Users\\Administrator\\IdeaProjects\\billing\\'+ picturename)
    report = "https://billing-dashboard.s3.amazonaws.com/" + picturename
    return report

def Sorted_Csv(results, type, nrows):
    data = pd.read_csv(results)
    x = results.split(".")
    print(x[0])
    sorted_file = x[0] + '-' + "sorted" + '-' + ".csv"
    print(sorted_file)
    sorted = data.sort_values(['TimePeriod', 'LinkedAccount', 'Amount'], ascending=[True, False, False]).groupby(['TimePeriod', 'LinkedAccount']).head(nrows)
    print(data.columns)
    output = sorted.to_csv(sorted_file, index=False)
    return sorted_file

def upload_file(fileupload):
    session = boto3.Session(profile_name='rnd')
    s3 = session.resource('s3')
    s3.Object('billing-dashboard', fileupload).upload_file(Filename='C:\\Users\\Administrator\\IdeaProjects\\billing\\'+ fileupload)
    report = "https://billing-dashboard.s3.amazonaws.com/" + fileupload
    return report

def generate_bar_charts_Service_region(outfile, cost):
    df = pd.read_csv(outfile)
    plt.figure(figsize=(20, 10))
    print(cost)
    sns.barplot(y='Amount', x=cost, hue='LinkedAccount', data=df)
    barfilename  = outfile + '.' + '.png'
    plt.savefig(barfilename)
    plt.show()
    return(barfilename)


if __name__ == '__main__':

    date_entry = input('Enter a date in YYYY-MM-DD format')
    year, month, day = map(int, date_entry.split('-'))
    end_date = datetime.date(year, month, day)
    print("is the end_date", end_date)
    start_date = FindMonths(end_date, -6)
    print("is the start_date", start_date)
    results, fetchdata = Generate_Cost_Csv(start_date, end_date)
    print(results)
    print("Please find the cost file", results)
    picturename = generate_bar_charts(results, fetchdata)
    url = upload_barchart(picturename)
    print("the url formed is", url)
    fileurls = []
    fileurls.append(url)
    typeCosts = ["REGION", "SERVICE"]
    for typecost  in typeCosts:
        outfile = Generate_Cost_Service_Region(start_date, end_date, typecost)
        sorted_file = Sorted_Csv(outfile, type, 5)
        print("sortedfile",sorted_file)
        fileupload_url = upload_file(sorted_file)
        print(fileupload_url)
        fileurls.append(fileupload_url)
        Costs = ["REGION", "SERVICE"]
    for cost  in Costs:
        start_date_month = FindMonths(end_date, -1)
        print("the start_date_monlty gor one month",start_date_month)
        outfilemonth = Generate_Cost_Service_Region(start_date_month, end_date, cost)
        sorted_file = Sorted_Csv(outfilemonth, cost, 3)
        print("The sorted file for 3 rows", sorted_file)
        barfilename = generate_bar_charts_Service_region(sorted_file, cost)
        print("the bar file name is", barfilename)
        reporturl = upload_file(barfilename)
        print("The reporturl is", reporturl)
        final_url = "https://billing-dashboard.s3.amazonaws.com/" + reporturl
        fileurls.append(final_url)
    Message_teams(results, fetchdata, fileurls)

