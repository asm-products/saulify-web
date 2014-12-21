import io

from saulify import sitespec


def specload_verifier(input_str, expected_out):
    infile = io.StringIO(input_str)
    actual_out = sitespec.load_rules(infile)
    assert actual_out == expected_out


def test_loading_basic_directives():
    specload_verifier(u"""
        title: //title
        body: //div[contains(@class, 'imageContainer')]
    """, {
        "title": [
            "//title"
        ],
        "body": [
            "//div[contains(@class, 'imageContainer')]"
        ],
    })


def test_ignored_lines():
    specload_verifier(u"""
        title: //title

        body: //div[contains(@class, 'imageContainer')]
        #body: //div[contains(@class, 'imageContainer')]


        test_url: http://example.com
    """, {
        "title": [
            "//title"
        ],
        "body": [
            "//div[contains(@class, 'imageContainer')]"
        ],
    })


def test_loading_repeated_directives():
    specload_verifier(u"""
        title://*[contains(@class,'post-title')]
        body://div[contains(@class,'post-body')]
        body://div[contains(@class,'entry-content')]
    """, {
        "title": [
            "//*[contains(@class,'post-title')]"
        ],
        "body": [
            "//div[contains(@class,'post-body')]",
            "//div[contains(@class,'entry-content')]"
        ]
    })


def test_loading_find_replace():
    specload_verifier(u"""
        find_string: <script type="text/javascript">
        replace_string: <div style="display:none;">
        find_string: </script>
        replace_string: </div>
    """, {
        "find_replace": [
            ('<script type="text/javascript">', '<div style="display:none;">'),
            ("</script>", "</div>")
        ],
    })
