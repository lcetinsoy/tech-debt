from subprocess import check_output
from shlex import split

def run_command(cmd):

    res = check_output(split(cmd))
    return res


def php_stan_plugin(folder, level, phpstan_path="vendor/bin/phpstan"):

    """
        run php stan for static analyse
        get the output as json
    """

    cmd = "{} analyse --level={} --error-format=json folder".format(phpstan_path, level, folder)

    json_report = run_command(cmd)
    report = json.loads(json_report)

    return php_stan_analyse_debt(report)


def php_stan_analyse_debt(report, options):

    return report['totals']['file_errors'] * options['score']

def score_error(error, scores):

    if "Call to an undefined" in error:
        return scores['undefined_function_call']

    return scores['default']
