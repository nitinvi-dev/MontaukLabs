import os
import uuid
import sys

from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
from pynamodb.models import Model
from pynamodb.attributes import *

path = sys.path[0].replace("/python-modules", "")+'/.env'
load_dotenv(path)

class Employers(Model):
    class Meta:
        table_name = f'{os.getenv("TABLE_NAME")}-labs'
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
        aws_region = os.getenv("AWS_REGION")

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)

    plan_id = UnicodeAttribute(null=True)
    plan_name = UnicodeAttribute(null=True)
    plan_type = UnicodeAttribute(null=True)

    ttl = NumberAttribute(null=True)

def get_current_timestamp():
    timestamp = datetime.timestamp(datetime.now() + relativedelta(years=1))
    return round(timestamp)

def clean_table():
    for x in Employers.scan():
        x.delete()

def ingest_data_sets():
    clean_table()
    for filename in os.listdir("data"):
        fObj = os.path.join("data", filename)
        if os.path.isfile(fObj) and "_index" in fObj:
            response = json.load(open(fObj))
            data = response["reporting_structure"][0]["reporting_plans"][0]
            employer_id = uuid.uuid4().__str__()
            Employers(
                pk=f"Employer#{employer_id}",
                sk=f"Employer#{employer_id}#plan#{data['plan_id']}",
                plan_name=data["plan_name"],
                plan_type=data["plan_id_type"],
                plan_id=data["plan_id"],
                files=response["reporting_structure"][0]["in_network_files"],
                ttl=get_current_timestamp()
            ).save()

if __name__ == '__main__':
    ingest_data_sets()