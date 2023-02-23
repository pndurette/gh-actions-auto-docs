import os
import re
import sys

import markdown
import yaml


try:
    # Read inputs
    ACTION_YAML_FILE = os.environ["ACTION_YAML_FILE"]
    OUTPUT_MD_FILE = os.environ["OUTPUT_MD_FILE"]
except KeyError as e:
    print(f"Missing {str(e)} environment varirable!")
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
    # render code blocks preperly in tables as <pre></pre
    md = re.sub("<code.*?>|<\/code>", "", md)

    # Convert remaining newlines to HTML breaks <br />
    # i.e. within multi-line html elements such as <p> or <pre>
    md = "<br />".join(md.splitlines())

    return md


def write_markdown(conf: dict, filename: str) -> None:
    try:
        with open(filename, "w") as f:
            # Header
            f.write("|Input|Description|Default|Required|\n")
            f.write("|-----|-----------|-------|:------:|\n")

            # https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#inputs
            for k, v in conf["inputs"].items():
                # <input_id> (required)
                input_id = f"`{k}`"

                # <input_id>.description (required)
                # <input_id>.deprecationMessage (optional)
                if "deprecationMessage" in v:
                    desc = f"{v['description']}\n\n**Depricated:** {v['deprecationMessage']}"
                desc = markdown_to_github_html_for_table(desc)

                # <input_id>.default (optional)
                default = f"`{v['default']}`" if "default" in v else "n/a"

                # <input_id>.required (optional)
                required = v["required"] if "required" in v else False
                required = "yes" if required else "no" 

                # Write markdown line
                f.write(f"|{input_id}|{desc}|{default}|{required}|\n")
    except Exception as e:
        print("Error:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    conf = read_action_yaml(ACTION_YAML_FILE)
    write_markdown(conf, OUTPUT_MD_FILE)
