# airos_scraper

The purpose of this file is to scrape data off of the airos 8 webpage created when trying to connect to the ubiquiti radios.

This program was designed to work on a Windows Powershell Environment (Although hopefully the software moves over to Linux in the future)

To start, make a new folder, clone the repo in the folder, make a file named `credentials.py`, open a Powershell terminal, and then `cd` into the directory where the repo is cloned.

## Expected File Structure
```
Folder PATH listing for volume OS
Volume serial number is C07F-B87E
C:.
│   credentials.py #Contains all of the private sign in credentials
│   
└───airos_scraper
        README.md
        requirements.txt
        scraper.py
```

## Dependencies
Ensure that Python3 is installed through the Microsoft appstore and then check that pip is updated by entering the following into Powershell:

`python3 -m pip install --upgrade pip`

To install webscraper dependencies, ensure you are in the project repo and type the following:

`pip3 install -r requirements.txt`

## System Parameters
Add sign in information to the new `credentials.py` file.
```
IP                     = '<GS IP HERE>'
USERNAME               = 'GO'
PASSWORD               = 'BLUE!'
```

Change the parameters in `airos_scraper/scraper.py` as needed

```
LOADING_DELAY            = 10 # Time to wait for the website to load on startup
LOGGING_FILENAME         = "<LOG_FILE_NAME>.txt"
RECORDING_PERIOD_SECONDS = n  # time in seconds between each data log.
```

## Usage

In the repo's directory, type `python3 .\scraper.py` to run the script. 

When logging is done, type `ctrl + c` to kill the process and stop logging. A `.txt` file in the repo will contain the log data. 

By default the log file will be called `signal_log.txt`, make sure to change the `LOGGING_FILENAME` variable to be the desired variable name.

## Potential Pain Points

This program uses [selenium](https://selenium-python.readthedocs.io/index.html) to get data from a website. Essentially, a browser opens in the background and that browser can receive commands through Python and send data back to the Python process. 

The major pain points with this approach are listed below:

Selenium will try to make get the web page for the airos login screen by trying `driver.get(f'http:{IP}/login.cgi')`. If this doesn't work, the value in the string might have to be changed to be able to get the login screen. Try changing the string to different URLs to get the data.

Grabbing elements from an HTML page is done by using `driver.find_element(...)`. If this line of code does not work, open inspect element (`ctrl + shift + c`) and look for the element that needs to be accessed. The [selenium locating elements](https://selenium-python.readthedocs.io/locating-elements.html) page is a great resource for this. Below is an example of finding elements by their path in the HTML document which will be a good reference if something does not work.

NOTE: The following example references the HTML code below, make sure to generalize this to the airos html page if things don't work.

For example, if there is an input element nested in a form element in the html page, locating by xpath is the ideal method.

```
<html>
 <body>
  <form id="loginForm">
   <input name="username" type="text" /> # We want to get this input element location in the HTML document
   <input name="password" type="password" />
   <input name="continue" type="submit" value="Login" />
   <input name="continue" type="button" value="Clear" />
  </form>
</body>
</html>
```

Use `username = driver.find_element(By.XPATH, "//form[input/@name='username']")` to get the location of the input for the username section and then use `username.send_keys(USERNAME)` to send the username to that input element.

To submit the username, do `submit = driver.find_element(By.XPATH, "//form[input/@value='Login']")` to get the location of the submit button element's value field and then use `submit.click()` to "click" on the button to submit the data.

Another problem that might occur would be that the webscraper cannot get into the webpage because it is stuck on an expired SSL certificate warning. The following can be done to fix these issues:

        - Have the webscraper connect to this page `https://expired.badssl.com/` and then test different selenium flags.
        - Add delays to wait for the website to load before making any calls to get data.
