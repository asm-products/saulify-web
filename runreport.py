from __future__ import print_function
import io
import os
import json
import argparse
import colorama

from saulify import sitespec
from saulify.testcase import TestCase

SPEC_DIRECTORY = "sitespecs"

colorama.init()
logger_green = colorama.Fore.GREEN
logger_red = colorama.Fore.RED
logger_yellow = colorama.Fore.YELLOW

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pretty", help="Pretty print test results",
                    action="store_true")
parser.add_argument("-v", "--verbose", help="Verbose print test results",
                    action="store_true")
args = parser.parse_args()

reports, passings, failings, warnings, exceptions = [], [], [], [], []


def test_passed(report):
    """ Whether all components of a scraper test succeeded """

    if report["status"] != "OK":
        return False

    for result in report["result"].values():
        if result["missing"]:
            return False

    return True


def generate_report(report):
    """ Prints test report dictionary as a colored character and generates summary of test """

    if report["status"] == "OK":
        result = "PASS" if test_passed(report) else "FAIL"
    elif report["status"] == "WARNING":
        result = "WARNING"
    else:
        result = "EXCEPTION"

    result_colors = {
        "PASS": logger_green,
        "FAIL": logger_red,
        "WARNING": logger_yellow,
        "EXCEPTION": logger_red
    }

    result_characters = {
        "PASS": 'p',
        "FAIL": 'f',
        "WARNING": 'w',
        "EXCEPTION": 'e'
    }

    # Print w/o newlines or spaces
    print(result_colors[result] + result_characters[result], end='')

    # Generate report summary based on type
    url_string = "Url: {0}; ". format(report["url"])
    if report["status"] == "EXCEPTION":
        exceptions.append(url_string + report["message"])

    elif report["status"] == "WARNING":
        warnings.append(url_string + report["message"])

    elif test_passed(report):
        r = report["result"]
        stats = ", ".join(["{0} {1}".format(len(r[c]["found"]), c) for c in r])
        passings.append(url_string + "Found: " + stats)

    else:
        for category, result in report["result"].items():
            if result["missing"]:
                count = len(result["missing"])
                missing = url_string + "Missing {0} {1}:\n".format(count, category)
                for item in result["missing"]:
                    missing += item + "\n"
                failings.append(missing)


def print_test_summary():
    passing_count, failing_count, warning_count, exception_count = len(passings), len(failings), len(warnings), len(exceptions)

    if args.verbose:
        print(logger_green + "\nPassing ({0})\n".format(passing_count))
        if passings:
            for test in passings:
                print(test)

        print(logger_red + "\nFailing ({0})\n".format(failing_count))
        if failings:
            for test in failings:
                print(test)

        print(logger_yellow + "\nWarnings ({0})\n".format(warning_count))
        if warnings:
            for test in warnings:
                print(test)

        print(logger_red + "\nExceptions ({0})\n".format(exception_count))
        if exceptions:
            for test in exceptions:
                print(test)

    print('\n-----------------------------\n' +
          '\nTest Summary:\n' +
          logger_green + 'Passing: {0}\n'.format(passing_count) +
          logger_red + 'Failing: {0}\n'.format(failing_count) +
          logger_yellow + 'Warnings: {0}\n'.format(warning_count) +
          logger_red + 'Exceptions: {0}\n'.format(exception_count) +
          '\n')


if __name__ == "__main__":
    spec_count = len([name for name in os.listdir(SPEC_DIRECTORY)])
    print('\n-----------------------------\n' +
          'Running {0} sitespec tests...\n'.format(spec_count) +
          '-----------------------------\n')
    for fname in os.listdir(SPEC_DIRECTORY):
        fpath = os.path.join(SPEC_DIRECTORY, fname)
        with io.open(fpath, encoding="utf-8") as f:
            test_specs = sitespec.load_testcases(f)
            for test_spec in test_specs:
                test_case = TestCase(test_spec)
                report = test_case.run()
                if args.pretty:
                    generate_report(report)
                else:
                    print(json.dumps(report))
    print(colorama.Fore.RESET + '\n\n-----------------------------\n')
    if args.pretty:
        print_test_summary()
