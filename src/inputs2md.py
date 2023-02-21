import os
import re
import sys

import markdown
import yaml

if "ACTION_YAML" not in os.environ:
    print("Missing ACTION_YAML environment varirable!")
    sys.exit(1)

if "OUTPUT_MD" not in os.environ:
    print("Missing OUTPUT_MD environment varirable!")
    sys.exit(1)


def read_action_yaml(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print("Error:", str(e))
        sys.exit(1)


def markdown_to_github_html_for_table(md: str) -> str:
    # Convert markdown to html
    # Support code blocks w/ fenced_code
    md = markdown.markdown(md, extensions=["fenced_code"])

    # Minify html tags
    md = re.sub(">\s*<", "><", md)

    # Strip <code ..> and </code> html tags
    # The 'fenced_code' python-markdown extension renders markdown
    # code blocks as <pre><code ...></code></pre> but GitHub will only
    # render code blocks preperly in tables as <pre></pre>
    md = re.sub("<code.*?>|<\/code>", "", md)

    # Convert remainling newlines to HTML breaks <br />
    # i.e. within multi-line html elements such as <p> or <pre>
    md = "<br />".join(md.splitlines())

    return md


def write_markdown(conf: dict, filename: str) -> None:
    try:
        with open(filename, "w") as f:
            # Header
            f.write("|Input|Description|Required|Default|\n")
            f.write("|-----|-----------|--------|-------|\n")

            # https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#inputs
            for k, v in conf["inputs"].items():
                # <id> (required)
                id = f"`{k}`"

                # <id>.description (required)
                desc = v["description"]
                desc = markdown_to_github_html_for_table(desc)

                # <id>.required (optional)
                required = v["required"] if "required" in v else False
                required = f"`{str(required).lower()}`"

                # <id>.default (optional)
                default = v["default"] if "default" in v else "N/A"
                default = f"`{default}`"

                # <id>.depreciationMessage (optional) TODO

                # Write markdown line
                f.write(f"|{id}|{desc}|{required}|{default}|\n")
    except Exception as e:
        print("Error:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    conf = read_action_yaml(os.environ["ACTION_YAML"])
    write_markdown(conf, os.environ["OUTPUT_MD"])
