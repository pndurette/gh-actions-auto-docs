# auto-doc-action

> A GitHub Action for generating GitHub Action markdown documentation

## Documentation

<!--doc_begin-->
### Inputs
|Input|Description|Default|Required|
|-----|-----------|-------|:------:|
|`action_yaml_file`|The path to GitHub Action's `action.yml` file|`./action.yml`|no|
|`include_inputs`|Test|`true`|no|
|`include_outputs`|Test|`true`|no|
|`heading_size`|Test|`3`|no|
|`template_file`|Test|`./README.md`|no|
|`target_file`|Test|`./README.md`|no|
|`marker_start`|Test|`<!--doc_begin-->`|no|
|`marker_end`|Test|`<!--doc_end-->`|no|
|`git_push`|If true it will commit and push the changes|`false`|no|
|`git_push_user_name`|If empty the name of the GitHub Actions bot will be used (i.e. `github-actions[bot]`)|`github-actions[bot]`|no|
|`git_push_user_email`|If empty the no-reply email of the GitHub Actions bot will be used (i.e. `github-actions[bot]@users.noreply.github.com`)|`github-actions[bot]@users.noreply.github.com`|no|
|`git_commit_message`|Commit message|`GitHub Action auto-doc`|no|
### Outputs
None
<!--doc_end-->

### Licence

[The MIT License (MIT)](LICENSE) Copyright © 2023 Pierre Nicolas Durette