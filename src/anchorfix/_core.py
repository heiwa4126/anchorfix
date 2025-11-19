import os
import sys
from dataclasses import dataclass


@dataclass
class PythonInfo:
    version: str
    executable_path: str
    script_path: str


def anchorfix() -> PythonInfo:
    return PythonInfo(
        version=sys.version,
        executable_path=sys.executable,
        script_path=os.path.abspath(__file__),
    )


def format_python_info(info: PythonInfo) -> str:
    return f"""Python Version: {info.version}
Executable Path: {info.executable_path}
Script Path: {info.script_path}
"""
