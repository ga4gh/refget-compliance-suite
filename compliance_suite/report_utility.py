import json

def generate_json_file(final_json, json):
    if json is None:
        return
    with open(json + '.json', 'w') as outfile:
        json.dump(final_json, outfile)


def generate_html_file(final_json, html):
    pass
