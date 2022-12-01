import pandas as pd
from datetime import datetime, timedelta
from scipy.integrate import quad
import collections
from datetime import date



# Calculates the density/point estimate of the Beta-distribution
def dbeta(x,shape1,shape2):
    """
    Calculates the density/point estimate of the Beta-distribution
    """
    from scipy.stats import beta
    result=beta.pdf(x=x,a=shape1,b=shape2,loc=0,scale=1)
    return result

# Calculates the cumulative of the Beta-distribution
def pbeta(q,shape1,shape2):
    """
    Calculates the cumulative of the Beta-distribution
    """
    from scipy.stats import beta
    result=beta.cdf(x=q,a=shape1,b=shape2,loc=0,scale=1)
    return result


# Calculates the Bayesian probability (i.e. the bandit recommendation)
def best_binominal_bandit(x, n, alpha=1, beta=1):
    ans = []
    k = len(x)
    l = list(range(0, k))
    for i in l:
        excluded_index = i
        indx = l[:excluded_index] + l[excluded_index + 1:]

        def f(z):
            r = dbeta(z, x[i] + alpha, n[i] - x[i] + beta)
            for j in indx:
                r = r * pbeta(z, x[j] + alpha, n[j] - x[j] + beta)
            return r

        a = quad(f, 0, 1)[0]
        ans.append(a)

    return ans

# Creating an alias
bbb = best_binominal_bandit


# Inputs the Distribution History and a mapping table (Distribution - MessageId) returns a dictionary with the bandit recommendation
def analyze_run_bandit(distribution_history, distribution_allocations):

    df = distribution_history

    df2 = distribution_allocations


    df2.rename(columns={'sendDate': 'key'}, inplace=True)
    df2['key'] = pd.to_datetime(df2['key'])

    # Exclude Survey Link and Survey Frequency from the original df
    df1 = df[['contactId', 'contactLookupId', 'distributionId', 'status',
              'responseId', 'responseCompletedAt', 'sentAt', 'openedAt',
              'responseStartedAt', 'surveySessionId']]

    df2.rename(columns={'distributionID': 'distributionId'}, inplace=True)
    df1.rename(columns={'responseCompletedAt': 'response_exact', 'sentAt': 'sent_exact', 'openedAt': 'opened_exact',
                        'responseStartedAt': 'started_exact'}, inplace=True)

    # Set the datetime format for the dates
    # 0.1.1

    df1 = df1[['contactId', 'contactLookupId', 'distributionId',
               'surveySessionId', 'responseId', 'status', 'sent_exact',
               'opened_exact', 'started_exact', 'response_exact']]

    # //0.4.1 Datetime Adjustments
    df1['sent_exact'] = pd.to_datetime(df1['sent_exact'])
    df1['key'] = df1['sent_exact']
    df1['opened_exact'] = pd.to_datetime(df1['opened_exact'])
    df1['response_exact'] = pd.to_datetime(df1['response_exact'])
    df1['started_exact'] = pd.to_datetime(df1['started_exact'])

    # //00 Date - Day
    df1['sent_day'] = pd.to_datetime(df1['sent_exact']).dt.dayofyear
    df1['opened_day'] = pd.to_datetime(df1['opened_exact']).dt.dayofyear
    df1['response_day'] = pd.to_datetime(df1['response_exact']).dt.dayofyear
    df1['started_day'] = pd.to_datetime(df1['started_exact']).dt.dayofyear

    # //00 Date - Week
    df1['sent_week'] = pd.to_datetime(df1['sent_exact']).dt.weekofyear
    df1['opened_week'] = pd.to_datetime(df1['opened_exact']).dt.weekofyear
    df1['response_week'] = pd.to_datetime(df1['response_exact']).dt.weekofyear
    df1['started_week'] = pd.to_datetime(df1['started_exact']).dt.weekofyear

    # //00 Date - Month
    df1['sent_month'] = pd.to_datetime(df1['sent_exact']).dt.month
    df1['opened_month'] = pd.to_datetime(df1['opened_exact']).dt.month
    df1['response_month'] = pd.to_datetime(df1['response_exact']).dt.month
    df1['started_month'] = pd.to_datetime(df1['started_exact']).dt.month

    # //00 Date - Year
    df1['sent_year'] = pd.to_datetime(df1['sent_exact']).dt.year
    df1['opened_year'] = pd.to_datetime(df1['opened_exact']).dt.year
    df1['response_year'] = pd.to_datetime(df1['response_exact']).dt.year
    df1['started_year'] = pd.to_datetime(df1['started_exact']).dt.year

    # column_names = list(df1.columns.values)
    # //Merge
    df1['key'] = pd.to_datetime(df1['key']).dt.date
    df2['key'] = pd.to_datetime(df2['key']).dt.date

    df2 = df2[['distributionId', 'messageID', 'count']]
    df1 = df1.merge(df2, on='distributionId', how='left')
    
    # We condition on "opened" anyways, so this should not be of any effect.
    #df1 = df1.drop(df1[df1.status == 'HardBounce'].index)
    #df1 = df1.drop(df1[df1.status == 'SoftBounce'].index)
    #df1 = df1.drop(df1[df1.status == 'Failure'].index)
    #df1 = df1.drop(df1[df1.status == 'Blocked'].index)

    df1 = df1.iloc[1:, :]
    # We are only regarding those that had at least 7 days to answer
    today = datetime.today()
    cutoff = today.date() - timedelta(days=0)  # eventually this should be 7! it is 40 now, since the Distribution history file is not up to date
    #print(df1)
    df1 = df1[(df1['sent_exact'].dt.date < cutoff)]
    #print(df1)


    df1['timedelta'] = df1['opened_exact'] - df1['sent_exact']

    df1.reset_index().to_feather(
        "A:/Data/GermanBusinessPanelTeam/Gaul/01_Tasks/01_Analysis_Questionnaire_Performance/01_Data/03_Bandit/" + "rawall_" + date.today().strftime("%Y-%m-%d") + ".feather")

    cutoff2 = timedelta(days=6, hours=20) #Adapted this, since it could be that for some the reminder is simply sent out earlier than the invite by chance.
    df1 = df1[(df1['timedelta'] < cutoff2)]
    #print(df1)
    Treatments = df1['messageID'].tolist()
    Treatments = list(set(Treatments))
    #print(Treatments)
    N = []
    X = []
    d = dict()

    df1.reset_index().to_feather(
        "A:/Data/GermanBusinessPanelTeam/Gaul/01_Tasks/01_Analysis_Questionnaire_Performance/01_Data/03_Bandit/" + "raw_" + date.today().strftime(
            "%Y-%m-%d") + ".feather")

    for element in Treatments:
        df_Analysis = df1[(df1['messageID'] == element)]
        n = df_Analysis['opened_exact'].count()
        x = df_Analysis['started_exact'].count()
        #print(df_Analysis)
        N.append(n)
        X.append(x)

        d.update({element: [n, x]})
        # d[element].get(element, []) + [x]

        #print(element)
        #print(x)
        #print(n)

    results = bbb(X, N)

    i = 0
    for element in Treatments:
        d[element].append(results[i])
        d[element].append(1000)
        d[element].append(round(results[i] * 1000))
        i = i + 1

    sorted_d = sorted(d.items(), key=lambda r: r[1][2])

    sorted_dict = collections.OrderedDict(sorted_d)
    d = sorted_dict
    df_out = pd.DataFrame.from_dict(d, orient='index')
    df_out.to_csv("A:/Data/GermanBusinessPanelTeam/Gaul/01_Tasks/01_Analysis_Questionnaire_Performance/01_Data/03_Bandit/" + "MAB_output_" + date.today().strftime("%Y-%m-%d") + ".csv")

    return d

'''
distribution_history = pd.read_csv('A:/Data/GermanBusinessPanelTeam/Gaul/01_Tasks/01_Analysis_Questionnaire_Performance/01_Data/03_Bandit/2022-11-11/Invite_2022-11-11.csv')

##TODO: Append each week!
filelist = ['2022-08-16.csv', '2022-08-17.csv', '2022-08-18.csv', '2022-08-19.csv',
                '2022-08-22.csv', '2022-08-23.csv', '2022-08-24.csv', '2022-08-25.csv', '2022-08-26.csv',
                '2022-08-29.csv', '2022-08-30.csv', '2022-08-31.csv', '2022-09-01.csv', '2022-09-02.csv',
                '2022-09-05.csv', '2022-09-06.csv', '2022-09-07.csv', '2022-09-08.csv', '2022-09-09.csv',
                '2022-09-12.csv', '2022-09-13.csv', '2022-09-14.csv', '2022-09-15.csv', '2022-09-16.csv',
                '2022-09-19.csv', '2022-09-20.csv', '2022-09-21.csv', '2022-09-22.csv', '2022-09-23.csv',
                '2022-09-26.csv', '2022-09-27.csv', '2022-09-28.csv', '2022-09-29.csv', '2022-09-30.csv',
                '2022-10-04.csv', '2022-10-05.csv', '2022-10-06.csv', '2022-10-07.csv',
                '2022-10-10.csv', '2022-10-11.csv', '2022-10-12.csv', '2022-10-13.csv', '2022-10-14.csv',
                '2022-10-17.csv', '2022-10-18.csv', '2022-10-19.csv', '2022-10-20.csv', '2022-10-21.csv',
                '2022-10-24.csv', '2022-10-25.csv', '2022-10-26.csv', '2022-10-27.csv', '2022-10-28.csv',
                '2022-11-02.csv', '2022-11-03.csv', '2022-11-04.csv',
                '2022-11-07.csv', '2022-11-08.csv', '2022-11-09.csv', '2022-11-10.csv', '2022-11-11.csv',
                '2022-11-14.csv', '2022-11-15.csv', '2022-11-17.csv', '2022-11-18.csv',
                '2022-11-21.csv', '2022-11-22.csv', '2022-11-23.csv', '2022-11-24.csv', '2022-11-25.csv']

distribution_allocations = pd.DataFrame()
for file in filelist:
    df = pd.read_csv('Z:/C01/Tax and Accounting Survey/Runde 5/Distributions/'+file)
    #print(file)
    #print(df)
    distribution_allocations = distribution_allocations.append(df)

d = analyze_run_bandit(distribution_history, distribution_allocations)

print(d)

'''