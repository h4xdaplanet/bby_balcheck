# Bestbuy Balance Check
Very basic script that uses the Bestbuy balance check frontend to check a CSV file of giftcards. 
The script iterates through the CSV file of giftcards and updates the Bal column. The script recycles the browser every 19 checks which is how I was getting a new IP from my proxy.

#### The column names in the CSV file must remain the same. See sample.csv for structure

## Setup
* Install requirements.txt
* Rename config.sample.py > config.py 
* Set proxy information and input/output filenames in config
* Run main.py
