import os
from tempfile import NamedTemporaryFile

import pytest

from actiondocs import ActionDocs

# Default options to use when they're not directly tested
DEFAULT_OPTIONS = {
    "include_inputs": True,
    "include_outputs": True,
    "heading_size": 3,
    "marker_start": "<!--start_test-->",
    "marker_end": "<!--end_test-->",
}


@pytest.fixture()
def dummy_action_file():
    """Generate a dummy action_file yaml for ActionDoc

    ActionDocs requires an actual yaml file as its 'action_file'
    Generate a fake file (but real on disk). Tests can then override
    the object attribute directly instead of loading from a real file.
    """
    action_file = NamedTemporaryFile("w", delete=True)
    action_file.write("test:")
    yield action_file.name
    action_file.close()


@pytest.fixture()
def dummy_template_file():
    """Generate a dummy template file for ActionDoc

    ActionDocs requires an actual file as its 'template_file'
    Generate a fake file (but real on disk). Tests can then override
    the object attribute directly instead of loading from a real file.
    """
    template_file = NamedTemporaryFile("w", delete=True)
    yield template_file.name
    template_file.close()


def test_input_simple(dummy_action_file, dummy_template_file):
    """Test simple (single-line values) input to Markdown"""
    action_config = {"inputs": {"in1": {"description": "desc"}}}
    expected_md = """|Input|Description|Default|Required|
|-----|-----------|-------|:------:|
|`in1`|desc|n/a|no|"""

    ad = ActionDocs(
        action_file=dummy_action_file,
        template_file=dummy_template_file,
        **DEFAULT_OPTIONS,
    )
    assert ad._get_markdown_table_inputs(action_config) == expected_md


def test_input_optionals(dummy_action_file, dummy_template_file):
    """Test simple (single-line values with optional values) input to Markdown"""
    action_config = {
        "inputs": {"in1": {"description": "desc", "default": "abc", "required": True}}
    }
    expected_md = """|Input|Description|Default|Required|
|-----|-----------|-------|:------:|
|`in1`|desc|`abc`|yes|"""

    ad = ActionDocs(
        action_file=dummy_action_file,
        template_file=dummy_template_file,
        **DEFAULT_OPTIONS,
    )
    assert ad._get_markdown_table_inputs(action_config) == expected_md


def test_input_depreciation(dummy_action_file, dummy_template_file):
    """Test simple (with optional input depreciation) input to Markdown"""
    action_config = {
        "inputs": {"in1": {"description": "desc", "deprecationMessage": "abc"}}
    }
    expected_md = """|Input|Description|Default|Required|
|-----|-----------|-------|:------:|
|`in1`|<p>desc</p><p><strong>Depricated:</strong> abc</p>|n/a|no|"""

    ad = ActionDocs(
        action_file=dummy_action_file,
        template_file=dummy_template_file,
        **DEFAULT_OPTIONS,
    )
    assert ad._get_markdown_table_inputs(action_config) == expected_md


def test_output_simple(dummy_action_file, dummy_template_file):
    """Test simple (single-line values) output to Markdown"""
    action_config = {"outputs": {"out1": {"description": "desc"}}}
    expected_md = """|Output|Description|
|------|-----------|
|`out1`|desc|"""

    ad = ActionDocs(
        action_file=dummy_action_file,
        template_file=dummy_template_file,
        **DEFAULT_OPTIONS,
    )
    assert ad._get_markdown_table_outputs(action_config) == expected_md


def test_substitution_empty(dummy_action_file, dummy_template_file):
    """Test full template sub when there's nothing between markers"""
    action_config = {
        "inputs": {"in1": {"description": "desc"}},
        "outputs": {"out1": {"description": "desc"}},
    }
    template_doc = """Text before

<!--start_test-->
<!--end_test-->

Text after"""
    expected_doc = """Text before

<!--start_test-->
### Inputs
|Input|Description|Default|Required|
|-----|-----------|-------|:------:|
|`in1`|desc|n/a|no|
### Outputs
|Output|Description|
|------|-----------|
|`out1`|desc|
<!--end_test-->

Text after"""

    ad = ActionDocs(
        action_file=dummy_action_file,
        template_file=dummy_template_file,
        **DEFAULT_OPTIONS,
    )
    ad.action_config = action_config  # Override action config
    ad.template = template_doc  # Override template

    assert ad.generate() == expected_doc


def test_substitution_content(dummy_action_file, dummy_template_file):
    """Test full template sub when there's content between markers"""
    action_config = {
        "inputs": {"in1": {"description": "desc"}},
        "outputs": {"out1": {"description": "desc"}},
    }
    template_doc = """Text before

<!--start_test-->
Some
Lines
That
Should
Go
<!--end_test-->

Text after"""
    expected_doc = """Text before

<!--start_test-->
### Inputs
|Input|Description|Default|Required|
|-----|-----------|-------|:------:|
|`in1`|desc|n/a|no|
### Outputs
|Output|Description|
|------|-----------|
|`out1`|desc|
<!--end_test-->

Text after"""

    ad = ActionDocs(
        action_file=dummy_action_file,
        template_file=dummy_template_file,
        **DEFAULT_OPTIONS,
    )
    ad.action_config = action_config  # Override action config
    ad.template = template_doc  # Override template

    assert ad.generate() == expected_doc


def test_substitution_no_marker(dummy_action_file, dummy_template_file):
    """Test full template sub when there's no markers"""
    action_config = {
        "inputs": {"in1": {"description": "desc"}},
        "outputs": {"out1": {"description": "desc"}},
    }
    template_doc = """Text before

No Marker

Text after"""
    expected_doc = """Text before

No Marker

Text after"""

    ad = ActionDocs(
        action_file=dummy_action_file,
        template_file=dummy_template_file,
        **DEFAULT_OPTIONS,
    )
    ad.action_config = action_config  # Override action config
    ad.template = template_doc  # Override template

    assert ad.generate() == expected_doc
