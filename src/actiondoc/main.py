import re
import logging

import yaml

from .utils import markdown_to_github_html_for_table

# Logger
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class ActionDoc:
    """A GitHub Action Markdown docs generator"""

    def __init__(self, action_file: str):
        """Instantiates ActionDoc and loads Action configuration

        https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions

        Args:
            action_file: the GitHub Action action.yml file to read
        """
        self.conf = self._load(filename=action_file)

    def _load(self, filename: str) -> str:
        """Loads a YAML file"""
        with open(filename, "r") as f:
            return yaml.safe_load(f)

    def _inputs(self) -> dict:
        """Loads the 'inputs' of the Action configuration"""
        try:
            return self.conf["inputs"]
        except KeyError as e:
            raise NoSectionException(e)

    def _outputs(self) -> dict:
        """Loads the 'outputs' of the Action configuration"""
        try:
            return self.conf["outputs"]
        except KeyError as e:
            raise NoSectionException(e)

    def inputs_markdown_table(self) -> str:
        """Generates the Action's 'inputs' as a Markdown table

        Generates a GitHub-flavoured markdown table of
        the Action inputs configuration. Supports multi-line Markdown
        for the 'description' field by converting to specific minified HTML
        that GitHub is known to render correctly.

        Returns:
            Markdown table of the Action's inputs
        """
        try:
            inputs_conf = self._inputs()
        except NoSectionException as e:
            return "None"

        rows = []

        # Header
        rows.append("|Input|Description|Default|Required|")
        rows.append("|-----|-----------|-------|:------:|")

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

            # Append markdown rows
            rows.append(f"|{input_id}|{desc}|{default}|{required}|")

        # Join rows with newlines
        return "\n".join(rows)

    def outputs_markdown_table(self) -> str:
        """Generates the Action's 'outputs' as a Markdown table

        Generates a GitHub-flavoured markdown table of
        the Action outputs configuration. Supports multi-line Markdown
        for the 'description' field by converting to specific minified HTML
        that GitHub is known to render correctly.

        Returns:
            Markdown table of the Action's outputs
        """
        try:
            outputs_conf = self._outputs()
        except NoSectionException as e:
            return "None"

        rows = []

        # Header
        rows.append("|Output|Description|")
        rows.append("|------|-----------|")

        for k, v in outputs_conf.items():
            # <output_id> (required)
            output_id = f"`{k}`"

            # <output_id>.description (required)
            desc = markdown_to_github_html_for_table(v["description"])

            # Append markdown line
            rows.append(f"|{output_id}|{desc}|")

        # Join rows with newlines
        return "\n".join(rows)

    def markdown(
        self, include_inputs=True, include_outputs=True, heading_size=3
    ) -> str:
        """Generates the full Action configuration as Markdown

        Generates a Markdown string of the following structure:
        <inputs title>
        <inputs Markdown table>

        <outputs title>
        <outputs Markdown table>

        Args:
            include_inputs: if the 'inputs' section should be included
            include_outputs: if the 'outputs' section should be included
            heading_size: the Markdown heading size for the section titles

        Returns:
            The full Markdown of the Action configuration
        """
        md = ""

        # Add inputs
        if include_inputs:
            md += f"{'#' * heading_size} Inputs"
            md += "\n"
            md += self.inputs_markdown_table()
            md += "\n"

        # Add output
        if include_outputs:
            md += f"{'#' * heading_size} Outputs"
            md += "\n"
            md += self.outputs_markdown_table()

        # Debug
        for index, line in enumerate(md.splitlines()):
            logging.debug(f"{index:03}: {line}")

        return md

    def insert_markdown(
        self,
        include_inputs: bool = True,
        include_outputs: bool = True,
        heading_size: int = 3,
        target_file: str = "README.md",
        marker_start: str = "<!--doc_begin-->",
        marker_end: str = "<!--doc_end-->",
    ) -> None:
        """Inserts the Markdown between two markers in a file

        Inserts or replaces the lines between two markers in a file with the
        generated Action documentation markdown.

        Args:
            include_inputs: if the 'inputs' section should be included
            include_outputs: if the 'outputs' section should be included
            heading_size: the Markdown heading size for the section titles
            target_file: the name of the file in which the insert will take place
            marker_start: the opening marker from which the insert will take place
            marker_end: the closing marker to which the insert will take place
        """

        # Prepare markers for regex
        marker_start = re.escape(marker_start)
        marker_end = re.escape(marker_end)

        # Compile regex
        marker_regex = re.compile(rf"(?<={marker_start}).*(?={marker_end})", re.DOTALL)

        # Generate markdown to insert
        markdown_to_insert = self.markdown(
            include_inputs=include_inputs,
            include_outputs=include_outputs,
            heading_size=heading_size,
        )

        # Open file for read/write and insert markdown between markers
        # (wrapping in newlines to make sure the markers stay on their own line)
        with open(target_file, "r+") as f:
            contents = f.read()
            contents = marker_regex.sub("\n" + markdown_to_insert + "\n", contents)

            f.seek(0)
            f.write(contents)
            f.truncate()


class NoSectionException(Exception):
    pass
