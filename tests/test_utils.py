import os

from actiondoc.utils import markdown_to_github_html_for_table


def test_table_markdown():
    """Test main styles for GitHub tables Markdown"""
    input_md = """
test `inline code` here

```python
code line 1
code line 2
```

**bold**

*italics*

* item 1
* item 2

Normal
Text
"""
    expected_html = (
        "<p>test <code>inline code</code> here</p>"
        "<pre>code line 1<br />code line 2<br /></pre>"
        "<p><strong>bold</strong></p><p><em>italics</em></p>"
        "<ul><li>item 1</li><li>item 2</li></ul>"
        "<p>Normal<br />Text</p>"
    )

    assert markdown_to_github_html_for_table(input_md) == expected_html
