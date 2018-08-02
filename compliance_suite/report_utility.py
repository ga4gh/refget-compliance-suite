import json

REPORTS_DIR = 'reports/'


def generate_json_file(final_json, json_file_name):
    '''
    generates json file for machine readability
    '''
    if json is None:
        return
    with open(json_file_name + '.json', 'w+') as outfile:
        json.dump(final_json, outfile)


def generate_html_file(final_json, html_file_name):
    '''
    generates html file for compliance matrix
    '''
    pass
