# gh-actions-auto-docs

> A GitHub Action for generating GitHub Action documentation

[![Tests](https://github.com/pndurette/gh-actions-auto-docs/actions/workflows/test.yml/badge.svg)](https://github.com/pndurette/gh-actions-auto-docs/actions/workflows/test.yml)

## Features



## Setup

1. In your `README.md` (or anywhere you'd like), add the template markers where you want the documentation to be inserted:

```markdown
<!--doc_begin-->
<!--doc_end-->
```

2. Add `pndurette/gh-actions-auto-docs` to a workflow, for example:

```yaml
name: Generate Action Docs

on: [pull_request]

jobs:
  doc:
    runs-on: ubuntu-latest

    permissions:
      # Required to push changes!
      contents: write

    steps:
    - uses: actions/checkout@v3
      with:
        # Required to push changes!
        ref: ${{ github.event.pull_request.head.ref }}
    
    - uses: pndurette/gh-actions-auto-docs@v1
```

:warning: **Note the requirements for allowing the workflow to push to git!**

### Configuration

<!--doc_begin-->

#### Inputs
|Input|Description|Default|Required|
|-----|-----------|-------|:------:|
|`action_yaml_file`|The path to the GitHub Action's `action.yml` file|`./action.yml`|no|
|`include_inputs`|Whenever to document the action's inputs|`true`|no|
|`include_outputs`|Whenever to document the action's outputs|`true`|no|
|`heading_size`|<p>The Markdown heading size to use for the documented<br />sections (i.e. number of <code>#</code>)</p>|`3`|no|
|`template_file`|The file used as template|`./README.md`|no|
|`target_file`|<p>The resulting file of the template substitution.<br />To update in-place, this can be the same as <code>template_file</code>.</p>|`./README.md`|no|
|`marker_start`|<p>The opening marker from which the template substitution<br />will take place</p>|`<!--doc_begin-->`|no|
|`marker_end`|<p>The closing marker to which the template substitution<br />will take place</p>|`<!--doc_end-->`|no|
|`git_push`|Whenever to commit and push changes changes to `target_file`|`false`|no|
|`git_push_user_name`|The git user name to commit with|`github-actions[bot]`|no|
|`git_push_user_email`|The git user email to commit with|`github-actions[bot]@users.noreply.github.com`|no|
|`git_commit_message`|The git commit message|`GitHub Action Auto-Docs`|no|
|`git_commit_signoff`|Whenever to sign-off the git commit|`false`|no|

<!--doc_end-->

### Licence

[The MIT License (MIT)](LICENSE) Copyright © 2023 Pierre Nicolas Durette