import logging
import re

import yaml

from .utils import markdown_to_github_html_for_table

# Logger
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class ActionDocs:
    """A GitHub Action Markdown docs generator"""

    def __init__(
        self,
        action_file: str,
        include_inputs: bool = True,
        include_outputs: bool = True,
        heading_size: int = 3,
        template_file: str = "README.md",
        marker_start: str = "<!--doc_begin-->",
        marker_end: str = "<!--doc_end-->",
    ):
        """Load action configuration and template

        For action configuration attributes, see:
        https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions

        Args:
            action_file: the GitHub action action.yml file to read
            include_inputs: if the 'inputs' section should be included
            include_outputs: if the 'outputs' section should be included
            heading_size: the Markdown heading size for the section titles
            template_file: the name of the file with which the Markdown
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
        self.marker_start = marker_start
        self.marker_end = marker_end

        # action config
        self.action_config = self._load_yaml(action_file)

        # Template file
        self.template = self._load_text(template_file)

        # Debug (arguments)
        for k, v in locals().items():
            if k == "self":
                continue
            log.debug(f"Arg: {k} = '{v}'")

        # Debug (action config)
        log.debug(f"Action config: {self.action_config}")

    def _load_yaml(self, filename: str) -> dict:
        """Loads a YAML file"""
        try:
            with open(filename, "r") as f:
                return yaml.safe_load(f)
        except OSError as e:
            log.error(f"Error loading YAML '{filename}': {str(e)}")
            raise

    def _load_text(self, filename: str) -> str:
        """Loads a text file"""
        try:
            with open(filename, "r") as f:
                return f.read()
        except OSError as e:
            log.error(f"Error loading '{filename}': {str(e)}")
            raise

    def _get_markdown_table_inputs(self, config: dict) -> str:
        """Generates the action's 'inputs' as a Markdown table

        Generates a GitHub-flavoured markdown table of
        the action inputs configuration. Supports multi-line Markdown
        for the 'description' field by converting to specific minified HTML
        that GitHub is known to render correctly.

        Args:
            config: the action configuration

        Returns:
            Markdown table of the action's inputs
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
            # Strip any trailing end-of-line char from the action file
            # (e.g. trailing \n on multi-line yaml)
            rows.append(
                f"|{input_id.rstrip()}"
                f"|{desc.rstrip()}"
                f"|{default.rstrip()}"
                f"|{required.rstrip()}"
                f"|"
            )

        # Join rows with newlines
        return "\n".join(rows)

    def _get_markdown_table_outputs(self, config: dict) -> str:
        """Generates the action's 'outputs' as a Markdown table

        Generates a GitHub-flavoured markdown table of
        the action outputs configuration. Supports multi-line Markdown
        for the 'description' field by converting to specific minified HTML
        that GitHub is known to render correctly.

        Args:
            config: the action configuration

        Returns:
            Markdown table of the action's outputs
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
            # Strip any trailing end-of-line char from the action file
            # (e.g. trailing \n on multi-line yaml)
            rows.append(f"|{output_id.rstrip()}" f"|{desc.rstrip()}" f"|")

        # Join rows with newlines
        return "\n".join(rows)

    def _get_full_markdown(self, config: dict) -> str:
        """Generates the full action configuration as Markdown

        Generates a Markdown string of the following structure:
        <inputs title>
        <inputs Markdown table>

        <outputs title>
        <outputs Markdown table>

        Args:
            config: the action configuration

        Returns:
            The full Markdown of the action configuration
        """
        md = ""

        # Add inputs
        if self.include_inputs:
            md += f"{'#' * self.heading_size} Inputs"
            md += "\n"
            md += self._get_markdown_table_inputs(config)
            md += "\n"

        # Add output
        if self.include_outputs:
            md += f"{'#' * self.heading_size} Outputs"
            md += "\n"
            md += self._get_markdown_table_outputs(config)

        # Debug
        for line in md.splitlines():
            log.debug(f"md: {line}")

        return md

    def generate(self) -> str:
        """Inserts the Markdown between two markers in a file

        Inserts or replaces the lines between two markers in a file with the
        generated action documentation markdown.

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
        document = marker_regex.sub(
            "\n" + self._get_full_markdown(self.action_config) + "\n", self.template
        )

        return document

    def save(self, filename):
        """Writes the document to file

        Args:
            filename: the file to save the resulting document to
        """
        document = self.generate()

        try:
            with open(filename, "w") as f:
                f.write(document)
                log.info(f"Wrote to '{filename}'")
        except IOError as e:
            log.error(f"Error saving '{filename}': {str(e)}")
            raise
