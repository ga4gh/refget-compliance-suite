from flask import Flask, request, Response
import json
import os
import re
from utils import *

DATA =[]
CIRCULAR_CHROMOSOME_SUPPORT = True
SUBSEQUENCE_LIMIT = 400000
TRUNC512 = True

app = Flask(__name__)

DATA = set_data()

def get_sequence_obj(seq_id):
    '''
    get_sequence_obj is used to get the sequence object from DATA
    based on the checksum identifier passed in the URL.
    '''
    for this_seq_obj in DATA:
        if this_seq_obj.md5 == seq_id:
            return this_seq_obj
        if TRUNC512 is True and this_seq_obj.sha512 == seq_id:
            return this_seq_obj
    return None
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
    
    if "accept" in header_content and header_content["accept"] not in [accept_type,"*/*"]:
        # bad mock server: status = 200 when headers are incorrect  
        return Response(status=200)
    

    algorithms_supported = ["md5"]
    if TRUNC512: algorithms_supported.append("trunc512")
    
    # bad mock server: "service" key does not exist in the response
    service_info_resp = {
    "_service": {
        "circular_supported": CIRCULAR_CHROMOSOME_SUPPORT,
        "algorithms": algorithms_supported,
        "subsequence_limit": SUBSEQUENCE_LIMIT,
        "supported_api_versions": ["1.0"]
        }
    }
    
    # bad mock server: status = 400 when success
    return Response(response=json.dumps(service_info_resp),status=400,mimetype=accept_type)

@app.route('/sequence/<seq_id>/metadata', methods=['GET'])
def get_metadata(seq_id):
    header_content = request.headers
    accept_type = "application/vnd.ga4gh.refget.v1.0.0+json"
    if "accept" in header_content and header_content["accept"] not in [accept_type,"*/*"]:
        # bad mock server: status = 200 when headers are incorrect 
        return Response(status=200)
    sequence_obj = get_sequence_obj(seq_id)
    if not sequence_obj:
        # bad mock server: status = 200 when sequence is not found
        return Response(status=200)
    # bad mock server: "metadata" key does not exist in the response
    metadata_resp = {
        "_metadata":{
            "md5":sequence_obj.md5,
            "trunc512": sequence_obj.sha512 if TRUNC512 else None,
            "length": sequence_obj.size,
            "aliases":[]
        }} 
    # bad mock server: status = 400 when success 
    return Response(response=json.dumps(metadata_resp),status=400,mimetype=accept_type)

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
    4. response headers?
    5. get app, port from config
    """

    header_content = request.headers
    accept_type = "text/vnd.ga4gh.refget.v1.0.0+plain"
    # validate the accept header
    if "accept" in header_content and header_content["accept"] not in [accept_type,"*/*"]:
        # bad mock server: status = 200 when headers are incorrect
        return Response(status=200)
    
    # check if the sequence is present. If not, error = 404
    sequence_obj = get_sequence_obj(seq_id)
    if not sequence_obj:
        # bad mock server: status = 200 when sequence is not found
        return Response(status=200)

    # get start, end and range params
    start = request.args.get('start', default = None)
    end = request.args.get('end', default=None)
    RANGE_HEADER_PATTERN = re.compile(r'bytes=[0-9]*-[0-9]*$')
    if "range" in header_content:
        seq_range = header_content["Range"]
        # bad mock server: status = 404 when both start/end and range parameters are passed 
        if (start or end) and seq_range: 
            return Response(status=404)
        # bad mock server: status = 404 when range pattern is not as expected 
        if not RANGE_HEADER_PATTERN.match(seq_range):
            return Response(status=404)

        fbs = int(header_content['Range'].split('=')[1].split('-')[0])
        lbs = int(header_content['Range'].split('=')[1].split('-')[1])
        if (fbs > sequence_obj.size-1) or (fbs > lbs):
            """
            Note:  
            we are ignoring case where (lbs > sequence_obj.size-1), (lbs-fbs+1 > SUBSEQUENCE_LIMIT) to match the compliance_suite tests
            filtering the case where (fbs > lbs) : Sub-sequences of circular chromosomes across the origin may not be requested via the Range header
            """
            # since fbs and lbs <= SUBSEQUENCE_LIMIT-1, it is implied that the subsequence limit if any is satisfied
            # bad mock server: incorrect status = 400
            return Response(status=400)
        elif (lbs > sequence_obj.size-1) :
            lbs = sequence_obj.size
        # bad mock server: status = 200 while returning subsequence
        return Response(response=(sequence_obj.sequence[fbs:lbs+1]).encode("ascii"),status=200, mimetype=accept_type)

    if start or end:
        # if start or end params are present, return the filtered sequence
        # if start or end params are not 32 bit unsigned int, error = 400
        # if start > sequence length, error =400
        # if start > end and circular not implemented, error = 501 
        if start:
            # TO DO: check if start and end are 32 bit
            if not start.isdigit(): #checks if start is unsigned int
                # bad mock server: incorrect status 200
                return Response(status=200)
            start = int(start)
        else: start = 0

        if end:
            if not end.isdigit(): #checks if end is unsigned int
                # bad mock server: incorrect status 200
                return Response(status=200)
            end = int(end)
        else: end = sequence_obj.size

        if start >= sequence_obj.size or end > sequence_obj.size :
            # bad mock server: incorrect status 400
            return Response(status=400)
        elif start > end:
            if CIRCULAR_CHROMOSOME_SUPPORT == False:
                # bad mock server: incorrect status 416
                return Response(status=416)
            else:
                if sequence_obj.is_circular == False:
                    # bad mock server: incorrect status 500
                    return Response(status=500)
                else:
                    if len(sequence_obj.sequence[start:sequence_obj.size]+sequence_obj.sequence[0:end])>SUBSEQUENCE_LIMIT:
                        # bad mock server: incorrect status 400
                        return Response(status=400)
                    else:
                        # bad mock server: incorrect status 404
                        return Response(response=(sequence_obj.sequence[start:sequence_obj.size]+sequence_obj.sequence[0:end]).encode("ascii"),status=404,mimetype=accept_type)
        elif end-start >SUBSEQUENCE_LIMIT:
            # bad mock server: incorrect status 200
            return Response(status=200)
        # bad mock server: incorrect status 404
        return Response(response=(sequence_obj.sequence[start:end]).encode("ascii"),status=404,mimetype=accept_type)
    # bad mock server: incorrect status 500
    return Response(response=(sequence_obj.sequence).encode("ascii"), status=500,mimetype=accept_type)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8988)