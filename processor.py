'''
This will process the end-end functionality for code.
'''

import math
import os
import sys
import json
import requests
import random
import uuid
from pymongo import MongoClient
from sandbox import get_required_output

class Processor:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['prog-db']  # Database
        self.prog_status = self.db['prog_status']  # collection
        self.STATUS_RUNNING = "running"
        self.STATUS_SUCCESS = "success"
        self.STATUS_FAILURE = "failure"
    
    def gen_unique_id(self):
        prog_id = str(uuid.uuid4())
        return prog_id
    
    def is_present(self, prog_id):
        cursor = self.prog_status.find({"prog_id": prog_id})
        if cursor.count() > 0:
            return True
        else:
            return False        

    def update_into_mongo(self, prog_id, prog_lang, status):
        try:
            if not self.is_present(prog_id):
                prog_dict = {}
                prog_dict['prog_id'] = prog_id
                prog_dict['prog_lang'] = prog_lang
                prog_dict['prog_status'] = status
                self.prog_status.insert(prog_dict)
            else:
                cursor = self.prog_status.find({'prog_id':prog_id})
                for doc in cursor:
                    prog_id = doc['prog_id']
                    self.prog_status.update({"prog_id": prog_id}, {"$set": {"prog_status": status}})
        except Exception, e:
            print "Error: %s" %(str(e)) 

    def process(self, prog_lang, code, inp):
        # generate the unique id for each program
        prog_id = self.gen_unique_id()
        self.update_into_mongo(prog_id, prog_lang, self.STATUS_RUNNING)
        # run the program in sanbox mode
        result, status = get_required_output(prog_id, prog_lang, code, inp)
        print prog_id
        print result    
        # update the doc in mongodb
        if status:
            self.update_into_mongo(prog_id, prog_lang, self.STATUS_SUCCESS)
        else:
            self.update_into_mongo(prog_id, prog_lang, self.STATUS_FAILURE)
        return result
