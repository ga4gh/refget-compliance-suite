from flask import Flask, request, Response
import json
import os
import re
from utils import *
from unittests.constants import GOOD_SERVER_URL

DATA =[]
CIRCULAR_CHROMOSOME_SUPPORT = True
SUBSEQUENCE_LIMIT = 400000
TRUNC512 = True
good_server_host = GOOD_SERVER_URL.split("://")[1].split(":")[0]
good_server_port = GOOD_SERVER_URL.split("://")[1].split(":")[1].replace("/","")

app = Flask(__name__)

DATA = set_data()

'''
HTTP codes
200:"Success"
206:"Success. Filtered Subsequence"
303:"Redirect to a url where sequence can be retrieved"
400:"Bad Request",
401:"Unauthorized",
404:"Not Found",
406:"Not Acceptable",
416:"Range Not Satisfiable",
501:"Not Implemented"
'''
@app.route('/sequence/service-info', methods=['GET'])
def get_service_info():
    header_content = request.headers
    accept_type = "application/vnd.ga4gh.refget.v1.0.0+json"

    # validate the accept header
    if "accept" in header_content and header_content["accept"] not in [accept_type,"*/*"]:
        return Response(status=406)

    algorithms_supported = ["md5"]
    if TRUNC512: algorithms_supported.append("trunc512")
    service_info_resp = {
    "service": {
        "circular_supported": CIRCULAR_CHROMOSOME_SUPPORT,
        "algorithms": algorithms_supported,
        "subsequence_limit": SUBSEQUENCE_LIMIT,
        "supported_api_versions": ["1.0"]
        }
    }
    return Response(response=json.dumps(service_info_resp),status=200,mimetype=accept_type)

@app.route('/sequence/<seq_id>/metadata', methods=['GET'])
def get_metadata(seq_id):
    header_content = request.headers
    accept_type = "application/vnd.ga4gh.refget.v1.0.0+json"

    # validate the accept header
    if "accept" in header_content and header_content["accept"] not in [accept_type,"*/*"]:
        return Response(status=406)

    # if sequence is not present, error = 404
    sequence_obj = get_sequence_obj(seq_id, DATA, TRUNC512)
    if not sequence_obj:
        return Response(status=404)

    metadata_resp = {
        "metadata":{
            "md5":sequence_obj.md5,
            "trunc512": sequence_obj.sha512 if TRUNC512 else None,
            "length": sequence_obj.size,
            "aliases":[]
        }}  
    return Response(response=json.dumps(metadata_resp),status=200,mimetype=accept_type)

@app.route('/sequence/<seq_id>', methods=['GET'])
def get_sequence(seq_id):
    """
    TO DO: 
    1. redirection 303. (not tested in compliance_suite)
    2. Note: compliance_suite ignores the range if it is out of bounds or if > SUBSEQUENCE_LIMIT
    3. Ambiguous error code resolution in refget documentation:
        range:
            The server MUST respond with a Bad Request error if one or more ranges are out of bounds of the sequence.
            If the server supports circular chromosomes and the chromosome is not circular 
            or the range is outside the bounds of the chromosome the server shall return Range Not Satisfiable.

        start, end:
            The server MUST respond with a Bad Request error if start is specified and is larger than the total sequence length.
            If the server supports circular chromosomes and the chromosome is not circular 
            or the range is outside the bounds of the chromosome the server shall return Range Not Satisfiable.
    4. Should we validate the response headers in the compliance suite?
    5. check if start and end are 32 bit
    """
    header_content = request.headers
    accept_type = "text/vnd.ga4gh.refget.v1.0.0+plain"
    # validate the accept header
    if "accept" in header_content and header_content["accept"] not in [accept_type,"*/*"]:
        return Response(status=406)
    
    # check if the sequence is present. If not, error = 404
    sequence_obj = get_sequence_obj(seq_id, DATA, TRUNC512)
    if not sequence_obj:
        return Response(status=404)

    # get start, end and range params
    start = request.args.get('start', default = None)
    end = request.args.get('end', default=None)
    RANGE_HEADER_PATTERN = re.compile(r'bytes=[0-9]*-[0-9]*$')
    if "range" in header_content:
        seq_range = header_content["Range"]

        # if start/end and range parameters are passed, error = 400
        if (start or end) and seq_range: 
            return Response(status=400)

        if not RANGE_HEADER_PATTERN.match(seq_range):
            return Response(status=400)

        fbs = int(header_content['Range'].split('=')[1].split('-')[0])
        lbs = int(header_content['Range'].split('=')[1].split('-')[1])
        if (fbs > sequence_obj.size-1) or (fbs > lbs):
            """
            Note:  
            we are ignoring case where (lbs > sequence_obj.size-1), (lbs-fbs+1 > SUBSEQUENCE_LIMIT) to match the compliance_suite tests
            filtering the case where (fbs > lbs) : Sub-sequences of circular chromosomes across the origin may not be requested via the Range header
            """
            # since fbs and lbs <= SUBSEQUENCE_LIMIT-1, it is implied that the subsequence limit if any is satisfied
            return Response(status=416)
        elif (lbs > sequence_obj.size-1) :
            lbs = sequence_obj.size
        return Response(response=(sequence_obj.sequence[fbs:lbs+1]).encode("ascii"),status=206, mimetype=accept_type)

    if start or end:
        # if start or end params are present, return the filtered sequence
        # if start or end params are not 32 bit unsigned int, error = 400
        # if start > sequence length, error =400
        # if start > end and circular not implemented, error = 501 
        if start:
            if not start.isdigit(): #checks if start is unsigned int
                return Response(status=400)
            start = int(start)
        else: start = 0

        if end:
            if not end.isdigit(): #checks if end is unsigned int
                return Response(status=400)
            end = int(end)
        else: end = sequence_obj.size

        if start >= sequence_obj.size or end > sequence_obj.size :
            return Response(status=416)
        elif start > end:
            if CIRCULAR_CHROMOSOME_SUPPORT == False:
                return Response(status=501)
            else:
                if sequence_obj.is_circular == False:
                    return Response(status=416)
                else:
                    if len(sequence_obj.sequence[start:sequence_obj.size]+sequence_obj.sequence[0:end])>SUBSEQUENCE_LIMIT:
                        return Response(status=416)
                    else:
                        return Response(response=(sequence_obj.sequence[start:sequence_obj.size]+sequence_obj.sequence[0:end]).encode("ascii"),status=200,mimetype=accept_type)
        elif end-start >SUBSEQUENCE_LIMIT:
            return Response(status=416)
        return Response(response=(sequence_obj.sequence[start:end]).encode("ascii"),status=200,mimetype=accept_type)

    return Response(response=(sequence_obj.sequence).encode("ascii"), status=200,mimetype=accept_type)

if __name__=="__main__":
    app.run(host=good_server_host,port=good_server_port)