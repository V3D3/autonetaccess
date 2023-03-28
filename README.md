# autonetaccess
**Requires:** python3: requests

**Usage:** run using python (`python main.py`).

**Caution:** saves credentials in plaintext as `cred.json` in the directory from which it is executed. Changing permissions on this file is recommended.

## Automation
Steps for setting up a cron job:

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

##  Failure:
- Auth failure/JSON error? Run it manually again.
- crontab listing showed nothing? Are you using VS Code as your default editor? Please use a command-line editor. Temporarily change it back by exporting `EDITOR` and `VISUAL` to `vim`, `vi`, or `nano`. Then edit crontab again (step 3).
- Can't tell which failure it is? Check `/tmp/cron.log`. If it doesn't exist, cron has not executed the job.

## Contribution: PRs are welcome!
Possible features:
1. build automation of cron and power events into a one-run solution (automate.py)
    1b. allow disabling of cron job/authorizing
2. store creds in a more secure fashion. (use keyring)
3. make connection failures more graceful.
4. load a cat gif when successfully authorized

Historical/Contributions:
1. de-authorize before authorizing again: (netaccess does not seem to extend duration on reauthorizing).
By Dragon-S1: netaccess does not need deauth. Also, it rounds off auth to (currently) hour:03, so next trigger can be predicted and cycles saved.

2. reduce the extra disk read when writing credentials for the first time.
Fixed by Dragon-S1.

3. allow duration selection.
Removed from todos: hour selection seems unnecessary. Instead can build a pause feature, if we control scheduling.

4. handle json format errors.
Done by V3D3.

Contributors:
Akshat Meena (Dragon-S1)
Vedaant Arya (V3D3)