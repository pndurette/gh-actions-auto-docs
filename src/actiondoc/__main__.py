import json
import logging
import os
import sys

from .main import ActionDoc

# An entrypoint to generate Action documentation Markdown
# using environment variables as arguments
# Usage: python -m actiondoc

REQUIRED_ENV_VARS = [
    "ACTION_YAML_FILE",
    "INCLUDE_INPUTS",
    "INCLUDE_OUTPUTS",
    "HEADING_SIZE",
    "TEMPLATE_FILE",
    "TARGET_FILE",
    "MARKER_START",
    "MARKER_END",
]


def _load_env_vars():
    """ "Loads required environment variables

    Loads and validates variables from environment.
    If one or more is missing, error out with the list of missing
    variables and exit 1
    """
    env_vars = dict.fromkeys(REQUIRED_ENV_VARS)
    for var in REQUIRED_ENV_VARS:
        try:
            env_vars[var] = os.environ[var]
            logging.info(f"Read env. var.: '{var}' = '{env_vars[var]}'")
        except KeyError:
            logging.error(f"Can't read env. var.: '{var}'")
            pass

    if None in env_vars.values():
        missing_env_vars = [k for k, v in env_vars.items() if not v]
        missing_env_vars_len = len(missing_env_vars)
        missing_env_vars_str = ", ".join(map(str, missing_env_vars))
        logging.error(
            f"Missing environment "
            f"variable{'s' if missing_env_vars_len> 1 else ''}: "
            f"{missing_env_vars_str}"
        )
        sys.exit(1)
    else:
        return env_vars


def main():
    config = _load_env_vars()

    # Use json to load boolean strings into boolean types
    action_doc = ActionDoc(
        action_file=config["ACTION_YAML_FILE"],
        include_inputs=json.loads(config["INCLUDE_INPUTS"].lower()),
        include_outputs=json.loads(config["INCLUDE_OUTPUTS"].lower()),
        heading_size=int(config["HEADING_SIZE"]),
        template_file=config["TEMPLATE_FILE"],
        marker_start=config["MARKER_START"],
        marker_end=config["MARKER_END"],
    )
    action_doc.save(config["TARGET_FILE"])


if __name__ == "__main__":
    # Configure logging
    # Automatically enable debug when it is enabled in GitHub Actions:
    # https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/enabling-debug-logging
    if os.environ.get("ACTIONS_STEP_DEBUG") == "true":
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level)

    # Run
    main()
