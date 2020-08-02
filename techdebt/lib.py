import os
import re

def extract_debt_annotations(content, debt_annotation ='@debpt'):

    pattern = r'@debpt\((.*)\).*'
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





def list_file(folder, ext):

    paths = []
    for root, dirs, files in os.walk(folder):

        for file in files:
            if file.endswith(ext):
                paths.append(os.path.join(root, file))

    return paths




def get_all_debt_annotations(folder, extension):

    annotations = []

    files = list_file(folder, extension)

    for file in files:

        with open(file, 'r') as f:

            content = f.read()
        annotations += extract_debt_annotations(content)


    return annotations



def test_list_file():

    ext = ".py"
    folder = "."

    paths = list_file(folder, ext)

    assert(len(paths) > 0)


def test_extract_debt_annotations():

    content = """coucou 
    
    
    @debpt("sdsd": "sdsd")
    def lala():
        return 2
    
    
    @debpt("api": "parameters")
    
    """

    out = extract_debt_annotations(content)

    assert len(out) == 2

