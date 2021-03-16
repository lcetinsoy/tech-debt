import os
import re




def get_debt_from_plugins(plugins):

    outputs = []
    for plugin in plugins: 

        output = run_plugin(plugin)
        outputs.append(output)

    return outputs


def run_plugin(plugin):

    module_name = plugin['module_name']
    if 'analyse_function' in plugin:
        analyse_function_name = plugin['analyse_function']
    else:
        analyse_function_name = "plugin_analyse_debt"

    module = __import__(module_name)
    function = getattr(module, analyse_function_name)

    return function(plugin)

def extract_debt_annotations(content, debt_annotation='@debt'):
    """
    Extract debt annotations in a dictionnary containing
    raw annotation and the line

    :param content:
    :param debt_annotation:
    :return:
    """


    pattern = r'{}\(?([\'|\"\w+:?\s+\w+\'\"]*)\)?'.format(debt_annotation)

    matches = []
    for i_line, line in enumerate(content.split('\n')):

        match = re.findall(pattern, line)

        if len(match) > 0:
            matches.append({'annotation': match[0], 'line': i_line})

    return matches



def test_extract_debt_annotations():

    content = """coucou 

    @debt("sdsd": "sdsd")
    def lala():
        return 2


    @debt("api": "parameters")

    @debt

    """

    out = extract_debt_annotations(content)

    assert len(out) == 3

    content = """

    \@debt('lala': 'lala')    
    """
    out = extract_debt_annotations(content)

    assert out == [{'annotation': "'lala': 'lala'", 'line': 2} ]




def parse_annotation(str_annotation):


    if ":" in str_annotation:
        annotation_data = str_annotation.split(":")
        annotation_type = annotation_data[0].strip()
        annotation_comment = annotation_data[1].strip()

    else:
        annotation_type = str_annotation.strip()
        annotation_comment = ""

    annotation_type = annotation_type.replace('"', '').replace("'", "")
    annotation_comment = annotation_comment.replace('"', '').replace("'", "")


    return annotation_type, annotation_comment


def analyse_file_debt(file, folder, extension):


    file_debts = []
    with open(file, 'r', encoding='latin1') as f:
        content = f.read()

    annotations = extract_debt_annotations(content)

    for dict_annotation in annotations:

        debt_type, debt_comment = parse_annotation(dict_annotation['annotation'])
        debt = {
            'file': file,
            'folder': folder,
            'extension': extension,
            'debt_type': debt_type,
            'comment':debt_comment,
            'line': dict_annotation['line']
        }

        file_debts.append(debt)

    return file_debts


def get_file_extension(file_path):

    parts = file_path.split('.')
    return parts[len(parts) - 1]

def analyse_folder_debt(folder, extensions, exclusions = []):

    all_debt = []
    file_paths = list_file(folder, extensions, exclusions)

    for file_path in file_paths:

        extension = get_file_extension(file_path)

        all_debt += analyse_file_debt(file_path, folder, extension)

    return all_debt


def analyse_debt(folders, extensions, exclusions = []):

    debt = []
    for folder in folders:

        debt += analyse_folder_debt(folder, extensions, exclusions)

    return debt



def compute_debt_statistics(dict_annotations, scores = {}):

    """
    produce a statistical report of debt based
    on all parsed debt annotations

    :param dict_annotations:
    :return:
    """

    if len(dict_annotations) == 0:
        return {
            'total': 0
        }

    import numpy as np
    import pandas as pd

    df = pd.DataFrame(dict_annotations)

    df['score'] = np.nan

    def update_score(row):

        debt_type = row['debt_type']

        if debt_type in scores:
            row['score'] = scores[debt_type]

        return row

    df = df.apply(update_score, axis=1)


    return {
        "total": df['score'].sum(),
        "per_file_extension": df.groupby(['extension'])[['extension', 'score']].agg('sum').reset_index(),
        "per_type": df.groupby(['debt_type'])[['debt_type', 'score']].agg('sum').reset_index(),
        "per_folder": df.groupby(['folder'])[['folder', 'score']].agg('sum').reset_index(),
    }


def print_stats(stats):

    print('--- Summary ---')
    print('total:', stats['total'])
    for extension in stats['per_file_extension'].iterrows():
        print(extension[1]['extension'], ': ', extension[1]['score'])

    for extension in stats['per_folder'].iterrows():
        print(extension[1]['folder'], ': ', extension[1]['score'])


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



def plot_debt(debt_statistics):

    import matplotlib.pyplot as plt
    per_type = debt_statistics['per_type']
    per_folder = debt_statistics['per_folder']
    per_extension = debt_statistics['per_file_extension']

    f = plt.subplot(2, 2, 1)
    f.bar(per_type['debt_type'], per_type['score'])

    f = plt.subplot(2, 2, 2)
    f.bar(per_folder['folder'], per_folder['score'])

    f = plt.subplot(2, 2, 3)
    f.bar(per_extension['extension'], per_extension['score'])

    plt.show()
