import os
import json

import saulify.sitespec as sitespec

SPEC_DIRECTORY = "sitespecs"


if __name__ == "__main__":
    for fname in os.listdir(SPEC_DIRECTORY):
        fpath = os.path.join(SPEC_DIRECTORY, fname)
        test_cases = sitespec.load_testcases(fpath)
        for test_case in test_cases:
            result = test_case.run()
            print(json.dumps(result))
