import os
import sys

from .action import Action

try:
    # Read inputs
    ACTION_YAML_FILE = os.environ["ACTION_YAML_FILE"]
    OUTPUT_MD_FILE = os.environ["OUTPUT_MD_FILE"]
except KeyError as e:
    print(f"Missing {str(e)} environment varirable!")
    sys.exit(1)

action = Action(ACTION_YAML_FILE)

# print(action._inputs())
# print(action._outputs())

# print(action.inputs_markdown_table())
# print()
# print(action.outputs_markdown_table())

print(action.markdown())