List of all Instapaper scraping directives and their interpretations.
Grepped from the repository at https://github.com/fivefilters/ftr-site-config
Some documentation available at http://help.fivefilters.org/customer/portal/articles/223153-site-patterns


# Key

Before each directive, we state its level of support in the `InstapaperScraper`.

- S : Supported
- P : Planned
- U : Unsupported


# Article Components

(S) author
(S) body
(S) date
(S) title
(S) footnotes

(U) native_ad_clue


# Cleaning

(S) strip
(U) strip_comments
(S) strip_id_or_class
(S) strip_image_src

(U) convert_double_br_tags

(S) find_string
(S) replace_string

(U) tidy
(U) prune


# Navigation

(P) next_page_link
(P) single_page_link
(P) single_page_link_in_feed


# Testing

(S) test_contains
(S) test_url


# Unknown / Other

(U) autodetect_next_page
(U) autodetect_on_failure

(U) dissolve
