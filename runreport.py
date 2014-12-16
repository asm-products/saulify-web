import os
import json
import argparse

import saulify.sitespec as sitespec

SPEC_DIRECTORY = "sitespecs"


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pretty", help="Pretty print test results",
                    action="store_true")
args = parser.parse_args()


def test_passed(report):
    """ Whether all components of a scraper test succeeded """

    if report["status"] != "OK":
        return False

    for result in report["result"].values():
        if result["missing"]:
            return False

    return True


def print_report(report):
    """ Converts test report dictionary to a human-readable format """

    if report["status"] == "OK":
        result = "PASS" if test_passed(report) else "FAIL"
    else:
        result = "EXCEPTION"

    print("{0} : {1}".format(result, report["url"]))

    if report["status"] == "EXCEPTION":
        print(report["message"])

    elif test_passed(report):
        r = report["result"]
        stats = ", ".join(["{0} {1}".format(len(r[c]["found"]), c) for c in r])
        print("Found " + stats)

    else:
        for category, result in report["result"].items():
            if result["missing"]:
                count = len(result["missing"])
                print("Missing {0} {1}:".format(count, category))
                for item in result["missing"]:
                    print(item)


if __name__ == "__main__":
    for fname in os.listdir(SPEC_DIRECTORY):
        fpath = os.path.join(SPEC_DIRECTORY, fname)
        test_cases = sitespec.load_testcases(fpath)
        for test_case in test_cases:
            report = test_case.run()
            if args.pretty:
                print_report(report)
                print("\n")
            else:
                print(json.dumps(report))
