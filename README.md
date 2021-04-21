# Hive-SBI

python scripts for automation of Hive-SBI

## How to start

### Installation of needed packages

The following packages are needed, when running the scripts on Ubuntu:

```text
apt-get install libmariadbclient-dev
```

```text
pip3 install beem dataset mysqlclient future
```

Compile and install steembi, the helper library for all steembasicincome scripts

```text
python setup.py install
```

### Prepare the database

Create schemas with the following names:

* sbi
* sbi\_steem\_ops

Run the following commands to configure the tables.

```text
mysql -u username -p sbi < sql/sbi.sql
mysql -u username -p sbi_steem_ops < sql/sbi_steem_ops.sql
```

### Creating a service script

Main runner script can be automatically run through systemd:

```text
useradd -r -s /bin/false sbiuser
chown -R sbiuser:sbiuser /etc/sbi

cp systemd/sbirunner.service to /etc/systemd/system/


systemctl enable sbirunner
systemctl start sbirunner

systemctl status sbirunner
```

The blacklist script is run once a day:

```text
cp systemd/blacklist.service to /etc/systemd/system/
cp systemd/blacklist.timer to /etc/systemd/system/

systemctl enable blacklist.timer
systemctl start blacklist.timer

systemctl list-timers
```

## Config file for accesing the database

A file `config.json` needs to be created in the top-level project directory:

```text
{

        "databaseConnector": "mysql://user:password@localhost/sbi_steem_ops",
        "databaseConnector2": "mysql://user:password@localhost/sbi",
        "hive_blockchain": true,
        "mgnt_shares": {"josephsavage": 4, "holger80": 1}
}
```

For STEEM set hive\_blockchain to false.

## Running steembasicincome

The following scripts need to run:

```text
python3 sbi_upvote_post_comment.py
python3 sbi_store_ops_db.py
python3 sbi_transfer.py
python3 sbi_update_member_db.py
python3 sbi_store_member_hist.py
python3 sbi_update_post_count.py
python3 sbi_stream_post_comment.py
python3 sbi_check_delegation.py
```

Note: The configuration table needs one entry for any of the scripts to run.

