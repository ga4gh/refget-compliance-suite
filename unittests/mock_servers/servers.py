import json

from flask import request, Response
import re
from unittests.utils import get_sequence_obj, set_data

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


class GoodRefgetServerV1:

    def __init__(self):
        self.json_accept_types = ["application/vnd.ga4gh.refget.v1.0.0+json"]
        self.plain_accept_types = ["text/vnd.ga4gh.refget.v1.0.0+plain"]
        self.TRUNC512 = True
        self.INSDC = False
        self.GA4GH = False
        self.CIRCULAR_CHROMOSOME_SUPPORT = True
        self.SUBSEQUENCE_LIMIT = 400000
        self.DATA = set_data()

    @staticmethod
    def valid_accept_type(header_content, accept_types):
        if "accept" not in header_content:
            return True
        if any(accept for accept in header_content["accept"].split(',') if accept in accept_types + ["*/*"]):
            return True

    def get_service_info(self):
        header_content = request.headers
        # validate the accept header
        if not self.valid_accept_type(header_content, self.json_accept_types):
            return Response(status=406)

        algorithms_supported = ["md5"]
        if self.TRUNC512:
            algorithms_supported.append("trunc512")
        service_info_resp = {
            "service": {
                "circular_supported": self.CIRCULAR_CHROMOSOME_SUPPORT,
                "algorithms": algorithms_supported,
                "subsequence_limit": self.SUBSEQUENCE_LIMIT,
                "supported_api_versions": ["1.0"]
            }
        }
        return Response(response=json.dumps(service_info_resp), status=200, mimetype=self.json_accept_types[0])

    def get_metadata(self, seq_id):
        header_content = request.headers

        # validate the accept header
        if not self.valid_accept_type(header_content, self.json_accept_types):
            return Response(status=406)

        # if sequence is not present, error = 404
        sequence_obj = get_sequence_obj(seq_id, self.DATA, self.TRUNC512, self.GA4GH, self.INSDC)
        if not sequence_obj:
            return Response(status=404)

        metadata_resp = {
            "metadata": {
                "md5": sequence_obj.md5,
                "length": sequence_obj.size,
                "aliases": []
            }}
        if self.TRUNC512:
            metadata_resp["metadata"]["trunc512"] = sequence_obj.sha512
        if self.GA4GH:
            metadata_resp["metadata"]["ga4gh"] = sequence_obj.ga4gh
        if self.INSDC:
            metadata_resp["metadata"]["aliases"].append({'name': sequence_obj.insdc, 'naming_authority': 'insdc'})

        return Response(response=json.dumps(metadata_resp), status=200, mimetype=self.json_accept_types[0])

    def get_sequence(self, seq_id):
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
        # validate the accept header
        if not self.valid_accept_type(header_content, self.plain_accept_types):
            return Response(status=406)

        # check if the sequence is present. If not, error = 404
        sequence_obj = get_sequence_obj(seq_id, self.DATA, self.TRUNC512, self.GA4GH, self.INSDC)
        if not sequence_obj:
            return Response(status=404)

        # get start, end and range params
        start = request.args.get('start', default=None)
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
            if (fbs > sequence_obj.size - 1) or (fbs > lbs):
                """
                Note:  
                we are ignoring case where (lbs > sequence_obj.size-1), (lbs-fbs+1 > SUBSEQUENCE_LIMIT) to match the compliance_suite tests
                filtering the case where (fbs > lbs) : Sub-sequences of circular chromosomes across the origin may not be requested via the Range header
                """
                # since fbs and lbs <= SUBSEQUENCE_LIMIT-1, it is implied that the subsequence limit if any is satisfied
                return Response(status=416)
            elif lbs > sequence_obj.size - 1:
                lbs = sequence_obj.size
            return Response(response=(sequence_obj.sequence[fbs:lbs + 1]).encode("ascii"), status=206,
                            mimetype=self.plain_accept_types[0])

        if start or end:
            # if start or end params are present, return the filtered sequence
            # if start or end params are not 32 bit unsigned int, error = 400
            # if start > sequence length, error =400
            # if start > end and circular not implemented, error = 501
            if start:
                if not start.isdigit():  # checks if start is unsigned int
                    return Response(status=400)
                start = int(start)
            else:
                start = 0

            if end:
                if not end.isdigit():  # checks if end is unsigned int
                    return Response(status=400)
                end = int(end)
            else:
                end = sequence_obj.size

            if start >= sequence_obj.size or end > sequence_obj.size:
                return Response(status=416)
            elif start > end:
                if not self.CIRCULAR_CHROMOSOME_SUPPORT:
                    return Response(status=501)
                else:
                    if not sequence_obj.is_circular:
                        return Response(status=416)
                    else:
                        if len(sequence_obj.sequence[start:sequence_obj.size] + sequence_obj.sequence[
                                                                                0:end]) > self.SUBSEQUENCE_LIMIT:
                            return Response(status=416)
                        else:
                            return Response(response=(
                                        sequence_obj.sequence[start:sequence_obj.size] + sequence_obj.sequence[
                                                                                         0:end]).encode("ascii"),
                                            status=200, mimetype=self.plain_accept_types[0])
            elif end - start > self.SUBSEQUENCE_LIMIT:
                return Response(status=416)
            return Response(response=(sequence_obj.sequence[start:end]).encode("ascii"), status=200,
                            mimetype=self.plain_accept_types[0])

        return Response(response=sequence_obj.sequence.encode("ascii"), status=200, mimetype=self.plain_accept_types[0])


class GoodRefgetServerV2(GoodRefgetServerV1):

    def __init__(self):
        super(GoodRefgetServerV2, self).__init__()
        self.json_accept_types = ["application/vnd.ga4gh.refget.v2.0.0+json"]
        self.plain_accept_types = ["text/vnd.ga4gh.refget.v2.0.0+plain"]
        self.TRUNC512 = False
        self.CIRCULAR_CHROMOSOME_SUPPORT = True
        self.SUBSEQUENCE_LIMIT = 400000
        self.GA4GH = True
        self.INSDC = True
        self.DATA = set_data()

    def get_service_info(self):
        header_content = request.headers
        # validate the accept header
        if not self.valid_accept_type(header_content, self.json_accept_types):
            return Response(status=406)

        algorithms_supported = ["md5"]
        identifiers_supported = []
        if self.TRUNC512:
            algorithms_supported.append("trunc512")
        if self.INSDC:
            identifiers_supported.append("insdc")
        service_info_resp = {
            {
                "id": "refget.good.server.v2",
                "name": "The GA4GH Refget API V2",
                "type": {
                    "group": "org.ga4gh",
                    "artifact": "refget",
                    "version": "2.0.0"
                },
                "organization": {
                    "name": "European Nucleotide Archive",
                    "url": "https://www.ebi.ac.uk/ena"
                },
                "refget": {
                    "circular_supported": self.CIRCULAR_CHROMOSOME_SUPPORT,
                    "subsequence_limit": self.SUBSEQUENCE_LIMIT,
                    "algorithms":  algorithms_supported,
                    "identifier_types": identifiers_supported
                }
            }
        }
        return Response(response=json.dumps(service_info_resp), status=200, mimetype=self.json_accept_types[0])

    def get_metadata(self, seq_id):
        super().get_metadata(seq_id)

    def get_sequence(self, seq_id):
        super().get_sequence(seq_id)


class BadRefgetServerV1(GoodRefgetServerV1):

    def get_service_info(self):
        header_content = request.headers
        # validate the accept header
        if not self.valid_accept_type(header_content, self.json_accept_types):
            # bad mock server: status = 200 when headers are incorrect
            return Response(status=200)

        algorithms_supported = ["md5"]
        if self.TRUNC512:
            algorithms_supported.append("trunc512")

        # bad mock server: "service" key does not exist in the response
        service_info_resp = {
            "_service": {
                "circular_supported": self.CIRCULAR_CHROMOSOME_SUPPORT,
                "algorithms": algorithms_supported,
                "subsequence_limit": self.SUBSEQUENCE_LIMIT,
                "supported_api_versions": ["1.0"]
            }
        }

        # bad mock server: status = 400 when success
        return Response(response=json.dumps(service_info_resp), status=400, mimetype=self.json_accept_types[0])

    def get_metadata(self, seq_id):
        header_content = request.headers
        # validate the accept header
        if not self.valid_accept_type(header_content, self.json_accept_types):
            # bad mock server: status = 200 when headers are incorrect
            return Response(status=200)
        response = super().get_metadata(seq_id)
        print(response)
        print(response.status_code)
        print(response.status)
        if response.status_code != 200:
            # bad mock server: status = 200 when sequence is not found
            response.status = 200
            return response

        # bad mock server: "metadata" key does not exist in the response
        metadata_resp = {"_metadata": response.json["metadata"]}
        # bad mock server: status = 400 when success
        print(metadata_resp)
        return Response(response=json.dumps(metadata_resp), status=400, mimetype=self.json_accept_types[0])

    def get_sequence(self, seq_id):
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

        # validate the accept header
        if not self.valid_accept_type(header_content, self.json_accept_types):
            # bad mock server: status = 200 when headers are incorrect
            return Response(status=200)

        response = super().get_sequence(seq_id)

        # check if the sequence is present.
        if response.status_code != 200:
            # bad mock server: status = 200 when sequence is not found
            response.status = 200
        else:
            response.status = 400
        return response


class BadRefgetServerV2(GoodRefgetServerV2, BadRefgetServerV1):
    def __init__(self):
        super(GoodRefgetServerV2, self).__init__()

    def get_service_info(self):
        return super(BadRefgetServerV1, self).get_service_info()

    def get_metadata(self, seq_id):
        return super(BadRefgetServerV1, self).get_metadata()

    def get_sequence(self, seq_id):
        return super(BadRefgetServerV1, self).get_sequence()