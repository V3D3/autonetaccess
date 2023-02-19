# autonetaccess
Requires: python3: requests, urllib3

Usage: run using python (`python main.py`).

Caution: saves credentials in plaintext as `cred.json` in the directory from which it is executed. Changing permissions on this file is recommended.

Setting up automatic approval: set up a cron job. Steps:

0. Run the script once, so that `cred.json` is created.
1. Install cron (`cronie` - for `apt`-using distros, run `apt install cronie`).
2. Enable the cron daemon (systemd: `systemctl enable cronie && systemctl start cronie`, usually requires sudo)
3. Create a cron file (`crontab -e`)
4. Write the jobs:
```
15,45 * * * * python /path/to/netaccess/main.py >> /tmp/cron.log 2>&1
@reboot sleep 15 && python /path/to/netaccess/main.py
```
*Explanation: first line repeats auth every hour at 15 and 45 minutes, second line auths 15 seconds after a reboot.*

*Note: replace **path/to** with the path of the script.*

5. Save the file. Exit editor. This will write the crontab to the default location (`/var/spool/cron/{user}` usually).

6. Verify that crontab is correctly saved: `crontab -l`. That's all!

Failure:
- Auth failure/JSON error? Remove `cred.json` from the script folder. Run it manually again.
- crontab listing showed nothing? Are you using VS Code as your default editor? Please use a command-line editor. Temporarily change it back by exporting `EDITOR` and `VISUAL` to `vim`, `vi`, or `nano`. Then edit crontab again (step 3).
- Can't tell which failure it is? Check `/tmp/cron.log`. If it doesn't exist, cron has not executed the job.