|Input|Description|Required|Default|
|-----|-----------|--------|-------|
|`action_yaml`|The path to a YAML file associating redirect keys to URLs, e.g.:<br /><br /><pre>---<br />test1: https://www.bookcity.ca/<br />test2: https://www.gladdaybookshop.com<br /></pre>|`false`|`./action.yml`|
|`markdown_file`|<p>Default behaviour for '/' or any 404, can be either:<br />* a URL to redirect to<br />* a message to display<br /><br />|`false`|`./README.md`|
