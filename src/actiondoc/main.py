import logging
import re

import yaml

from .utils import markdown_to_github_html_for_table

# Logger
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class ActionDoc:
    """A GitHub Action Markdown docs generator"""

    def __init__(
        self,
        action_file: str,
        include_inputs: bool = True,
        include_outputs: bool = True,
        heading_size: int = 3,
        target_file: str = "README.md",
        marker_start: str = "<!--doc_begin-->",
        marker_end: str = "<!--doc_end-->",
    ):
        """Instantiates ActionDoc and loads Action configuration

        https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions

        Args:
            action_file: the GitHub Action action.yml file to read
            include_inputs: if the 'inputs' section should be included
            include_outputs: if the 'outputs' section should be included
            heading_size: the Markdown heading size for the section titles
            target_file: the name of the file in which the Markdown
                substitution will take place
            marker_start: the opening marker from which the substitution
                will take place
            marker_end: the closing marker to which the substitution
                will take place
        """
        # Arguments
        self.include_inputs = include_inputs
        self.include_outputs = include_outputs
        self.heading_size = heading_size
        self.target_file = target_file
        self.marker_start = marker_start
        self.marker_end = marker_end

        # Action config
        self.config = self._load(filename=action_file)

        # Debug (arguments)
        for k, v in locals().items():
            if k == "self":
                continue
            log.debug(f"Arg: {k} = '{v}'")

        # Debug (Action config)
        log.debug(f"Action configuration: {self.config}")

    def _load(self, filename: str) -> str:
        """Loads a YAML file"""
        with open(filename, "r") as f:
            return yaml.safe_load(f)

    def _inputs_markdown_table(self, config: dict) -> str:
        """Generates the Action's 'inputs' as a Markdown table

        Generates a GitHub-flavoured markdown table of
        the Action inputs configuration. Supports multi-line Markdown
        for the 'description' field by converting to specific minified HTML
        that GitHub is known to render correctly.

        Args:
            config: the Action configuration

        Returns:
            Markdown table of the Action's inputs
        """
        try:
            inputs_config = config["inputs"]
            log.info(f"Inputs: {len(inputs_config)}")
        except KeyError:
            log.info(f"Inputs: None")
            return "None"

        rows = []

        # Header
        rows.append("|Input|Description|Default|Required|")
        rows.append("|-----|-----------|-------|:------:|")

        for k, v in inputs_config.items():
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

    def _outputs_markdown_table(self, config: dict) -> str:
        """Generates the Action's 'outputs' as a Markdown table

        Generates a GitHub-flavoured markdown table of
        the Action outputs configuration. Supports multi-line Markdown
        for the 'description' field by converting to specific minified HTML
        that GitHub is known to render correctly.

        Args:
            config: the Action configuration

        Returns:
            Markdown table of the Action's outputs
        """
        try:
            outputs_config = config["outputs"]
            log.info(f"Outputs: {len(outputs_config)}")
        except KeyError:
            log.info(f"Outputs: None")
            return "None"

        rows = []

        # Header
        rows.append("|Output|Description|")
        rows.append("|------|-----------|")

        for k, v in outputs_config.items():
            # <output_id> (required)
            output_id = f"`{k}`"

            # <output_id>.description (required)
            desc = markdown_to_github_html_for_table(v["description"])

            # Append markdown line
            rows.append(f"|{output_id}|{desc}|")

        # Join rows with newlines
        return "\n".join(rows)

    def _markdown(self) -> str:
        """Generates the full Action configuration as Markdown

        Generates a Markdown string of the following structure:
        <inputs title>
        <inputs Markdown table>

        <outputs title>
        <outputs Markdown table>

        Returns:
            The full Markdown of the Action configuration
        """
        md = ""

        # Add inputs
        if self.include_inputs:
            md += f"{'#' * self.heading_size} Inputs"
            md += "\n"
            md += self._inputs_markdown_table(self.config)
            md += "\n"

        # Add output
        if self.include_outputs:
            md += f"{'#' * self.heading_size} Outputs"
            md += "\n"
            md += self._outputs_markdown_table(self.config)

        # Debug
        for index, line in enumerate(md.splitlines()):
            log.debug(f"Markdown line {index:03}: {line}")

        return md

    def _full_document(self) -> str:
        """Inserts the Markdown between two markers in a file

        Inserts or replaces the lines between two markers in a file with the
        generated Action documentation markdown.

        Returns:
            the full substituted document
        """

        # Prepare markers for regex
        marker_start = re.escape(self.marker_start)
        marker_end = re.escape(self.marker_end)

        # Compile regex
        marker_regex = re.compile(rf"(?<={marker_start}).*(?={marker_end})", re.DOTALL)

        # Generate the final document (insert Markdown between markers)
        # (wrapping in newlines to make sure the markers stay on their own line)
        with open(self.target_file, "r") as f:
            document = marker_regex.sub("\n" + self._markdown() + "\n", f.read())

        return document

    def rewrite(self):
        """Writes the substituted to file"""
        full_document = self._full_document()
        with open(self.target_file, "w") as f:
            f.write(full_document)
            log.info(f"Wrote to '{self.target_file}'")
