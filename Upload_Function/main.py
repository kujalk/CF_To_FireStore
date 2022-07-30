import datetime
import json
import logging
import random
import string
from uuid import uuid4

import firebase_admin
import requests
import xmltodict
from firebase_admin import credentials, firestore, initialize_app
from firestore_batch import Batch

logging.basicConfig(format="%(asctime)s :: [%(module)s] :: [%(levelname)s] :: %(message)s",level="INFO")
logger = logging.getLogger('log')

# initializations 
firebase_admin.initialize_app()
db = firestore.client()

def get_country_list(url):
    """
    To get the the sanction list
    """
    
    try:
        data=requests.get(url)

        if(data.status_code == 200):
            logger.info(f"Country list return code is 200")
            
            obj = xmltodict.parse(data.text,attr_prefix='')
            
            logger.info(f"Total count of countries : {len(obj['mondial']['country'])}")
            
            return obj["mondial"]["country"]
                
        else:
            raise Exception (f"Unable to retrieve the data from url, and response is {data.text} and status code is {data.status_code}")

    except Exception as e:
        logger.error(f"Error while getting countries list {e}")
        raise Exception("e")

def write_batch_data(data):
    try:
        logger.info("Going to insert the data into Firestore")
        count = 0

        random_string=(''.join(random.choices(string.ascii_lowercase, k=5)))
        collection_name = f"{str(datetime.datetime.now().date())}_{random_string}"
        logger.info(f"Collection Name is {collection_name}")

        with Batch(db) as batch:

            for entry in data:

                count+=1
                logger.info(f"Inserting data - {count}")
                batch.set(db.collection(collection_name).document(str(uuid4())), entry)

    except Exception as e:
        logger.error(f"Error while inserting batch data - {e}")
        raise Exception (e)

#Main
def main(event,context):
    retrieved_data = get_country_list("http://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/mondial/mondial-3.0.xml")
    write_batch_data(retrieved_data)