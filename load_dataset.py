import sys
import os
import json
import xml.etree.ElementTree as ET

def load_dataset():
    if len(sys.argv) == 1:
        print("ERROR: need to specify a dataset")
        return

    dataset_name = sys.argv[1]
    dataset_path = os.path.join("searchindex", "datasets", f"{dataset_name}.xml")
    fixture_folder = os.path.join("searchengine", "fixtures")
    fixture_path = os.path.join(fixture_folder, f"{dataset_name}.json")

    os.makedirs(fixture_folder, exist_ok=True)

    with open(dataset_path) as f:
        with open(fixture_path, 'wt') as fixture:
            idx = 1
            fixture.write("[")
            for _, elem in ET.iterparse(f):
                if elem.tag == "row":
                    doc_id = elem.attrib["Id"]
                    text = elem.attrib["Body"].strip()
                    title = elem.attrib["Title"].strip()

                    if idx > 1:
                        fixture.write(",")

                    fixture_object = {
                        'model': 'searchengine.Document',
                        'pk': idx,
                        'fields': {
                            'doc_id': doc_id,
                            'text': text,
                            'title': title,
                        }
                    }

                    fixture.write(json.dumps(fixture_object))
                    
                    idx += 1

            fixture.write("]")

    from django.core.management import call_command
    call_command("flush", "--no-input")
    call_command("loaddata", f"{dataset_name}.json")

if __name__ == '__main__':
    load_dataset()