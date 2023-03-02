import logging

# GitHub Action Workflow Commands
# https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions

# TODO: Docs

class GHACommand:
    """A GitHub Action Worflow Command"""
    def __init__(self, cmd_name: str, cmd_value: str, **cmd_params) -> None:
        self.cmd_name = cmd_name
        self.cmd_value = cmd_value
        self.cmd_params = {k: str(v) for k, v in cmd_params.items()}

    def preflight(self) -> None:
        pass

    def output(self) -> str:
        self.preflight()
        if self.cmd_params:
            # If there's parameters, they should be printed as:
            # <space><k1>=<v1>,<k2>=<v2>,...
            cmd_params_lst = [f"{k}={v}" for k, v in self.cmd_params.items()]
            cmd_params_str = f" {','.join(cmd_params_lst)}"
        else:
            cmd_params_str = ""

        return f"::{self.cmd_name}{cmd_params_str}::{self.cmd_value}"


class GHAAnnotation(GHACommand):
    def preflight(self) -> None:
        ALLOWED_PARAMS = ["file", "line", "endLine", "title"]

        illegal_params = [p for p in self.cmd_params.keys() if p not in ALLOWED_PARAMS]
        if illegal_params:
            raise ValueError(illegal_params)

        if "line" in self.cmd_params:
            if not "file" in self.cmd_params:
                raise ValueError("'line' requires 'file'")

        if "endLine" in self.cmd_params:
            if not "line" in self.cmd_params:
                raise ValueError("'endLine' requires 'line'")


def debug(message: str) -> None:
    print(GHACommand(cmd_name="debug", cmd_value=message).output())


def notice(message: str, **kwargs) -> None:
    print(GHAAnnotation(cmd_name="notice", cmd_value=message, **kwargs).output())


def warning(message: str, **kwargs) -> None:
    print(GHAAnnotation(cmd_name="warning", cmd_value=message, **kwargs).output())


def error(message: str, **kwargs) -> None:
    print(GHAAnnotation(cmd_name="error", cmd_value=message, **kwargs).output())



class GHAFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        s = super().format(record)
        if record.levelno == logging.DEBUG:
            return GHACommand(cmd_name="debug", cmd_value=s).output()
        elif record.levelno == logging.WARNING:
            return GHAAnnotation(cmd_name="warning", cmd_value=s).output()
        elif record.levelno >= logging.ERROR:
            return GHAAnnotation(cmd_name="error", cmd_value=s).output()
        else:
            # There's no GitHub Actions Workflow command for INFO
            return s
