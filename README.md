# noip-confirmhostname
This is a simple Python script to confirm your free no-ip hostname(s).

# INSTALL
git clone 

## DEPENDENCIES
```
sudo apt-get -y install python
```
## HOWTO
 - Add your username and password to the script
 - Run 
 ```
 python no-ip_confirm_hostname.py
 ```
## AUTOMATE SCRIPT
  - Run 
  ```
  crontab -e
  ```
  - add line e.g "0 12 * * * $HOME/noip-confirmhostname/no-ip_confirm_hostname.py" to run the script daily at 12 am
