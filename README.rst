1. Python **3.9.0**


2. Set following variables to .env file to access DynamoDB. 
 
   - AWS_ACCESS_KEY
   - AWS_SECRET_KEY
   - AWS_REGION

3. Run below command to create DynamoDb table.

    - $ serverless deploy


4. Install dependency libraries:

    - $ pip install -r requirements.txt


5. Run vomit script to download files from page https://transparency-in-coverage.uhc.com

    - $ python python-modules/vomit.py


6. Ingest data to database from downloaded files:

    - $ python python-modules/ingest.py


7. Run flask App

    - $ python frontend/app.py


8. Run on browser:

    - http://127.0.0.1:5000
