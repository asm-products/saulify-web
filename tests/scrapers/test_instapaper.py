from lxml import html, etree

from collections import defaultdict

from saulify.scrapers.instapaper import InstapaperScraper


def clean_result_verifier(spec_dict, input_str, expected_out_str):

    def normalise(source):
        parser = etree.HTMLParser(remove_blank_text=True)
        norm_nodes = etree.HTML(source, parser)
        for elem in norm_nodes.iter('*'):
            if elem.text is not None:
                elem.text = elem.text.strip()
            if elem.tail is not None:
                elem.tail = elem.tail.strip()
        return html.tostring(norm_nodes)

    result = scrape_string(spec_dict, input_str)
    assert normalise(result["html"]) == normalise(expected_out_str)


def scrape_string(spec_dict, input_str):
    spec = defaultdict(list, spec_dict)
    scraper = InstapaperScraper(spec)
    return scraper.clean_article(input_str)


def test_strip_elements():
    clean_result_verifier({
        "strip": ['//div[@class="stripme"]']
    }, """
      <div>
        <div class="stripme" />
        <div>
          <div class="stripme" />
        </div>
      </div>
    """, """
      <div>
        <div></div>
      </div>
    """)


def test_extract_body():
    clean_result_verifier({
        "body": ['//div[@class="body"]']
    }, """
       <div>
           <div class="body">
               Article text
           </div>
           <div>
               Other stuff
           </div>
       </div>
    """, """
       <div class="body">
           Article text
       </div>
    """)


def test_strip_id_or_class():
    # This behaviour represents a literal reading of the fivefilters docs.
    clean_result_verifier({
        "strip_id_or_class": ['class1 class2']
    }, """
       <div>
           <div class="class1 class2"></div>
           <div class="class2 class1"></div>
           <div class="class1"></div>
           <div class="notclass1 class2"></div>
       </div>
    """, """
       <div>
           <div class="class2 class1"></div>
           <div class="class1"></div>
       </div>
    """)


def test_find_replace():
    clean_result_verifier({
        "find_replace": [("wrongtag", "div")]
    }, """
       <wrongtag>
         <div>Content</div>
       </wrongtag>
    """, """
       <div>
         <div>Content</div>
       </div>
    """)


def test_extract_field():
    input_str = """
    <div>
        <div class="author">
            John Smith
        </div>
    </div>
    """
    spec = {
        "author": ['//div[@class="author"]']
    }
    result = scrape_string(spec, input_str)
    assert result["author"] == ["John Smith"]


def test_extract_field_fallback():
    input_str = """
    <div>
        <div class="author">
            John Smith
        </div>
    </div>
    """
    spec = {
        "author": ['//div[@id="fails"]', '//div[@class="author"]']
    }
    result = scrape_string(spec, input_str)
    assert result["author"] == ["John Smith"]


def test_extract_field_multiple():
    input_str = """
    <div>
        <div class="author">
            John Smith
        </div>
        <div class="author">
            Joe Bloggs
        </div>
    </div>
    """
    spec = {
        "author": ['//div[@id="fails"]', '//div[@class="author"]']
    }
    result = scrape_string(spec, input_str)
    assert result["author"] == ["John Smith", "Joe Bloggs"]
