import os

from dotenv import load_dotenv
from pynamodb.models import Model
from pynamodb.attributes import *

load_dotenv("../.env")

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


def get_employers(q):
    data = []
    limit = os.getenv("LIMIT", 20)
    if q:
        for item in Employers.scan(
                filter_condition=(Employers.plan_name.startswith(q) | Employers.plan_type.startswith(q)),
                limit=limit):
            data.append(item.to_json())
    else:
        for item in Employers.scan(
                filter_condition=(Employers.pk.startswith("Employer#")),
                limit=limit):
            data.append(item.to_json())

    return {
        "data":data
    }