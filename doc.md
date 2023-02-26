# auto-doc-action

> A GitHub Action for generating GitHub Action markdown documentation

## Documentation

<!--doc_begin-->
### Inputs
|Input|Description|Default|Required|
|-----|-----------|-------|:------:|
|`action_yaml`|<p>The path to a <code>YAML</code> file associating redirect keys to URLs, e.g.:</p><pre>---<br />test1: https://www.bookcity.ca/<br />test2: https://www.gladdaybookshop.com<br /></pre><p><strong>Depricated:</strong> Omg stop using this!</p>|`./action.yml`|no|
|`markdown_file`|<p>Default behaviour for '/' or any 404, can be either:</p><ul><li>a URL to redirect to</li><li>a message to display</li></ul>|`./README.md`|no|
|`test1`|<p>Test:</p><ul><li>Item 1</li><li>Item 2</li></ul>|n/a|no|
|`test2`|<p>Test:</p><p>Some <strong>bold</strong> and some <em>italics</em>. ~~Scratch this.~~</p><p><a href="https://www.google.com">I'm an inline-style link</a></p><ol><li>Item 1</li><li>Item 2</li></ol>|n/a|no|
### Outputs
|Output|Description|
|------|-----------|
|`test1`|<p>a test1</p>|
<!--doc_end-->

### Licence

[The MIT License (MIT)](LICENSE) Copyright © 2023 Pierre Nicolas Durette