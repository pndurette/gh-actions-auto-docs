|Input|Description|Required|Default|
|-----|-----------|--------|-------|
|`action_yaml`|<p>The path to a YAML file associating redirect keys to URLs, e.g.:</p><pre>---<br />test1: https://www.bookcity.ca/<br />test2: https://www.gladdaybookshop.com<br /></pre>|no|`./action.yml`|
|`markdown_file`|<p>Default behaviour for '/' or any 404, can be either:</p><ul><li>a URL to redirect to</li><li>a message to display</li></ul>|no|`./README.md`|
|`test1`|<p>Test:</p><ul><li>Item 1</li><li>Item 2</li></ul>|no|n/a|
|`test2`|<p>Test:</p><p>Some <strong>bold</strong> and some <em>italics</em>. ~~Scratch this.~~</p><p><a href="https://www.google.com">I'm an inline-style link</a></p><ol><li>Item 1</li><li>Item 2</li></ol>|no|n/a|
