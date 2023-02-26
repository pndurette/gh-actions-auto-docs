import re

import markdown


def markdown_to_github_html_for_table(md: str) -> str:
    """
    Transforms Markdown into specific HTML that renders
    correctly in GitHub flavoured Markdown table cells.
    (e.g. code blocks)
    """

    # If the Markdown is one line, it can be rendered as-is
    if not "\n" in md:
        return md

    # Convert markdown to html
    # Support code blocks w/ fenced_code
    md = markdown.markdown(md, extensions=["fenced_code"])

    # Minify html tags
    md = re.sub(">\s*<", "><", md)

    # Strip <code ..> and </code> html tags when directly inside <pre></pre>
    # The 'fenced_code' python-markdown extension renders markdown
    # code blocks as <pre><code ...></code></pre> but GitHub will only
    # render code blocks preperly in tables as <pre></pre>.
    # <code></code> renders as (inline) code.
    md = re.sub("(?<=<pre>)<code.*?>|<\/code>(?=<\/pre>)", "", md)

    # Convert remaining newlines to HTML breaks <br />
    # i.e. within multi-line html elements such as <p> or <pre>
    md = "<br />".join(md.splitlines())

    return md
