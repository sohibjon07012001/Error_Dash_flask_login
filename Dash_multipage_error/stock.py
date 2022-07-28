from datetime import datetime, date, timedelta
import datetime as datetime_main
import dateutil.relativedelta
import pandas as pd




def partner_names1():
    df = pd.read_excel("Post_Analysis_Partners.xlsx")
    return df

def date_main(type_time):
    startday_daily = date.today().strftime('%Y-%m-%d')
    end_day = date.today().strftime('%Y-%m-%d')
    startday_weekly = (date.today() - datetime_main.timedelta(days=date.today().weekday())).strftime('%Y-%m-%d')
    startday_monthly = (date.today().replace(date.today().year, date.today().month, 1)).strftime('%Y-%m-%d')
    startday_annually = (date.today().replace(date.today().year, 1, 1)).strftime('%Y-%m-%d')

    start_day_lastday = []
    end_day_lastweek = []
    end_day_lastmonth = []
    end_day_lastyear = []
    for i in range(1, 2):
        start_day_lastday.append(date.today() - timedelta(days=i))
        end_day_lastweek.append(date.today() - datetime_main.timedelta(days=date.today().weekday()) - timedelta(days=i))
        end_day_lastmonth.append(datetime.strptime(startday_monthly, '%Y-%m-%d') - timedelta(days=i))
        end_day_lastyear.append(datetime.strptime(startday_annually, '%Y-%m-%d') - timedelta(days=i))

    startday_lastweek = (date.today() - datetime_main.timedelta(days=date.today().weekday(), weeks=1)).strftime(
        '%Y-%m-%d')
    startday_lastmonth = (date.today().replace((date.today() + dateutil.relativedelta.relativedelta(months=-1)).year,
                                               (date.today() + dateutil.relativedelta.relativedelta(months=-1)).month,
                                               1)).strftime('%Y-%m-%d')

    if type_time == "daily":
        return startday_daily, end_day
    elif type_time == "weekly":
        return startday_weekly, end_day
    elif type_time == "monthly":
        return startday_monthly, end_day
    elif type_time == "annually":
        return startday_annually, end_day
    elif type_time == "lastday":
        return start_day_lastday[0].strftime('%Y-%m-%d'), start_day_lastday[0].strftime('%Y-%m-%d')
    elif type_time == "lastweek":
        return startday_lastweek, end_day_lastweek[0].strftime('%Y-%m-%d')
    elif type_time == "lastmonth":
        return startday_lastmonth, end_day_lastmonth[0].strftime('%Y-%m-%d')
    elif type_time == "lastyear":
        return (date.today().replace(date.today().year - 1, 1, 1)).strftime('%Y-%m-%d'), end_day_lastyear[0].strftime(
            '%Y-%m-%d')


