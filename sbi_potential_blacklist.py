from beem import vote
from datetime import datetime
import pytz
from datetime import timedelta
import json
import dataset

if __name__ == "__main__":
    config_file = 'config.json'
    try:
        with open(config_file) as json_data_file:
            config_data = json.load(json_data_file)
    except FileNotFoundError:
        raise FileNotFoundError("config.json is missing!")

    # datetime object must be localized. Assuming Eastern Time
    yesterday = datetime.now() - timedelta(days=1)
    tz = pytz.timezone('US/Eastern')
    start_date = tz.localize(yesterday)

    votes = vote.AccountVotes('hivewatchers', start=start_date)

    # Down Votes have a weight of 0.
    down_voted_accounts = set()
    for vote in votes:
        if vote.weight == 0:
            down_voted_accounts.add(vote.votee)

    sbi_database_connector = config_data["databaseConnector2"]
    sbi_database = dataset.connect(sbi_database_connector)
    member_table = sbi_database['member']
    pending_blacklist_table = sbi_database['pending_blacklist']

    for down_voted_account in down_voted_accounts:
        if member_table.find_one(account=down_voted_account, hivewatchers=0) is not None:
            try:
                pending_blacklist_table.insert({'member_account': down_voted_account})
            except:
                print('User "{}" is already in pending_blacklist'.format(down_voted_account))
