from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
import requests
import json
import unicodecsv as csv
import os
import time


class EpaDataGetter(object):
    WATER_TYPE = 'WaterSystems'
    FACILITY_TYPE = 'Facilities'
    VALID_REQUEST_TYPES = (WATER_TYPE, FACILITY_TYPE)

    def __init__(self, requests_before_pause=3, pause_seconds=1):
        self.hostname = 'https://ofmpub.epa.gov/echo'
        # the system rate limits and this is crude without a nice retry system
        self.requests_before_pause = requests_before_pause
        self.pause_seconds = pause_seconds
        self.request_count = 0
        self.request_type = ''
        self.system_url = ''
        self.query_url = ''
        self.columns_query_param = ''

        # self.states = [
        #     "AL",  "AK",  "AS",  "AZ",  "AR",  "CA",  "CO",  "CT",
        #     "DE",  "DC",  "FM",  "FL",  "GA",  "GU",  "HI",  "ID",
        #     "IL",  "IN",  "IA",  "KS",  "KY",  "LA",  "ME",  "MH",
        #     "MD",  "MA",  "MI",  "MN",  "MS",  "MO",  "MT",  "NE",
        #     "NV",  "NH",  "NJ",  "NM",  "NY",  "NC",  "ND",  "MP",
        #     "OH",  "OK",  "OR",  "PW",  "PA",  "PR",  "RI",  "SC",
        #     "SD",  "TN",  "TX",  "UT",  "VT",  "VI",  "VA",  "WA",
        #     "WV",  "WI",  "WY"
        # ]

        self.states = [
            "CA"
        ]


    def collect_and_save_data(self, output_directory):
        if self.request_type not in EpaDataGetter.VALID_REQUEST_TYPES:
            raise ValueError('Invalid request type. Must be watersystem or facility.')

        for state in self.states:
            self.get_query_id_from_epa_system_url(state)
            if self.query_id is None:
                continue
            file_name = '%s.csv' %state
            target_file = os.path.join(output_directory, self.request_type, file_name)
            self.create_target_file(target_file) 
            data, page = True, 1
            while data:
                data = self.get_page_of_data_for_query_id(page)
                page += 1
                if data is not None:
                    self.append_data_to_file(data, target_file)
            

    def get_query_id_from_epa_system_url(self, state):
        """
        This expects an EPA endpoint that returns a query ID so we can then process the data separately.
        Just setting the property rather than returning a value but that feels weird.
        The assummption about query parameter names hopefully holds true for all endpoints like it has so far.
        """
        self.rate_limit_requests()
        url = '%s?output=JSON&p_st=%s&p_act=Y' % (self.system_url, state)
        print(url)
        data = self.get_json_data_from_url(url)
        print(data)
        if data is not None:
            data = data["Results"]
            query_rows = int(data["QueryRows"])
            query_id = data["QueryID"]
            if query_rows != 0 and query_id:
                self.query_id = query_id
                self.query_rows = query_rows
            else:
                self.query_id = None
                self.query_rows = None
        else:
            self.query_id = None
            self.query_rows = None


    def get_page_of_data_for_query_id(self, page_number):
        """
        It turns out the download endpoints are not thorough enough so we need to use the paginated data.
        The assummptions about query parameter names hopefully holds true for all endpoints like it has so far.
        """
        self.rate_limit_requests()
        url = '%s?output=JSON&qid=%s&pageno=%s%s' % (
            self.query_url, self.query_id, page_number, self.columns_query_param)
        # self.stdout.write(url) # not available unless this is in a command
        # should try/except here to handle timeouts, over hitting API
        print(url)
        data = self.get_json_data_from_url(url)
        # returns an empty array when past last page of data. It doesn't seem the API otherwise indicates??
        if not data["Results"]:
            return None
        elif not data["Results"][self.request_type]:
            return None
        else:
            return data["Results"][self.request_type]


    def get_json_data_from_url(self, url):
        raw_json = requests.get(url)
        if raw_json.status_code == 200:
            data = json.loads(raw_json.content)
        else:
            raise ValueError('Invalid response: %s %s' %
                            (raw_json.status_code, raw_json.content))
        return data


    def rate_limit_requests(self):
        self.request_count += 1
        if self.request_count % self.requests_before_pause == 0:
            time.sleep(self.pause_seconds)


    def create_target_file(self, target_file):
        with open(target_file, 'w'):
            pass  # just open the file to delete everything


    def append_data_to_file(self, data, target_csv):
        with open(target_csv, 'ab+') as f:
            csvwriter = csv.writer(f, encoding='utf-8')
            count = 0
            previous_data = os.stat(target_csv).st_size != 0
            for row in data:
                if not previous_data and count == 0:
                    header = row.keys()
                    csvwriter.writerow(header)
                    count += 1
                if self.should_write_row(row):
                    csvwriter.writerow(row.values())


    def should_write_row(self, row):
        return True

class EpaFacilityDataGetter(EpaDataGetter):

    def __init__(self):
        super(EpaFacilityDataGetter, self).__init__()
        self.request_type = EpaDataGetter.FACILITY_TYPE
        self.system_url = '%s/echo_rest_services.get_facilities' % self.hostname
        self.query_url = '%s/echo_rest_services.get_qid' % self.hostname
        # there are tons of columns and we don't need them all. This list was found using the metadata URL and then picking out interesting items
        # https://ofmpub.epa.gov/echo/echo_rest_services.metadata?output=JSON
        self.columns_query_param = r'&qcolumns=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C16%2C17%2C23%2C63%2C64%2C69%2C70%2C71%2C72%2C73%2C89%2C91%2C96%2C97%2C98%2C99%2C100%2C101%2C102%2C110%2C156%2C158%2C167%2C168%2C185%2C188'

    
    def should_write_row(self, row):
        # Indicates whether the facility has a Safe Drinking Water Information System (SDWIS) ID
        # We don't care about any facilities that aren't water related (could look for watershed info someday)
        return row["SDWISFlag"] == 'Y'

if __name__ == "__main__":
    getter = EpaFacilityDataGetter()
    getter.collect_and_save_data('fake')