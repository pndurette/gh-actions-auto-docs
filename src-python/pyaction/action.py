import yaml

from .utils import markdown_to_github_html_for_table

# https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#inputs


class Action:
    def __init__(self, action_file: str):
        self.conf = self._load(action_file)

    def _load(self, filename: str) -> str:
        with open(filename, "r") as f:
            return yaml.safe_load(f)

    def _inputs(self) -> dict:
        try:
            return self.conf["inputs"]
        except KeyError as e:
            raise NoSectionException(e)

    def _outputs(self) -> dict:
        try:
            return self.conf["outputs"]
        except KeyError as e:
            raise NoSectionException(e)

    def inputs_markdown_table(self) -> str:
        try:
            inputs_conf = self._inputs()
        except NoSectionException as e:
            return "None"

        lines = []

        # Header
        lines.append("|Input|Description|Default|Required|")
        lines.append("|-----|-----------|-------|:------:|")

        for k, v in inputs_conf.items():
            # <input_id> (required)
            input_id = f"`{k}`"

            # <input_id>.description (required)
            # <input_id>.deprecationMessage (optional)
            desc = v["description"]
            if "deprecationMessage" in v:
                desc += "\n\n" + f"**Depricated:** {v['deprecationMessage']}"
            desc = markdown_to_github_html_for_table(desc)

            # <input_id>.default (optional)
            default = f"`{v['default']}`" if "default" in v else "n/a"

            # <input_id>.required (optional)
            required = v["required"] if "required" in v else False
            required = "yes" if required else "no"

            # Append markdown line
            lines.append(f"|{input_id}|{desc}|{default}|{required}|")

        # Return with newlines
        return "\n".join(lines)

    def outputs_markdown_table(self) -> str:
        try:
            outputs_conf = self._outputs()
        except NoSectionException as e:
            return "None"

        lines = []

        # Header
        lines.append("|Output|Description|")
        lines.append("|------|-----------|")

        for k, v in outputs_conf.items():
            # <output_id> (required)
            output_id = f"`{k}`"

            # <output_id>.description (required)
            desc = markdown_to_github_html_for_table(v["description"])

            # Append markdown line
            lines.append(f"|{output_id}|{desc}|")

        # Return with newlines
        return "\n".join(lines)

    def markdown(self, inputs=True, outputs=True, header_size=3) -> str:
        md = ""

        if inputs:
            md += f"{'#' * header_size} Inputs"
            md += "\n"
            md += self.inputs_markdown_table()
            md += "\n"

        if outputs:
            md += f"{'#' * header_size} Outputs"
            md += "\n"
            md += self.outputs_markdown_table()

        return md

class NoSectionException(Exception):
    pass
