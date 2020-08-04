import os
import re

def extract_debt_annotations(content, debt_annotation ='@debt'):

    pattern = r'{}\((.*)\).*'.format(debt_annotation)
    matches = re.findall(pattern, content)

    return matches



def debt_statistics(str_annotations):

    parsed_annotations = {}

    for str_annotation in str_annotations:

        if ":" in str_annotation:

            annotation_type = str_annotation.split(":")[0]

        else:
            annotation_type = str_annotation


        annotation_type = annotation_type.replace("'", "").replace('"', "")
        if annotation_type in parsed_annotations:
            parsed_annotations[annotation_type] += 1

        else:
            parsed_annotations[annotation_type] = 1

    return parsed_annotations





def get_all_debt_annotations(folders, extensions, exclusions = []):

    annotations = []
    for folder in folders:

        annotations += get_folder_debt_annotations(folder, extensions, exclusions)

    return annotations




def get_folder_debt_annotations(folder, extensions, exclusions = []):

    annotations = []


    files = list_file(folder, extensions, exclusions)

    for file in files:

        with open(file, 'r', encoding='latin1') as f:

            content = f.read()
        annotations += extract_debt_annotations(content)


    return annotations




def list_file(folder, extensions, exclusions):

    paths = []
    for root, dirs, files in os.walk(folder):


        keep = True
        for exclusion in exclusions:
            if exclusion in root:
                keep = False

        if not keep:
            continue

        for file in files:

            parts = file.split('.')
            ext = "." + parts[len(parts) - 1]

            if ext in extensions:

                full_path = os.path.join(root, file)
                paths.append(full_path)

    return paths


def test_list_file():

    exts = [".py"]
    folder = "/home/zoubab/dev/tech-debt/techdebt"

    exclusions = []
    paths = list_file(folder, exts, exclusions)

    assert(len(paths) > 0)


def test_extract_debt_annotations():

    content = """coucou 
    
    
    @debt("sdsd": "sdsd")
    def lala():
        return 2
    
    
    @debt("api": "parameters")
    
    """

    out = extract_debt_annotations(content)

    assert len(out) == 2

