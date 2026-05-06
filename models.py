from pydantic import BaseModel
from typing import Literal , Any

from rich.style import Style

class SafetyStatus(BaseModel):
    safe: bool
    reason: str | None = None



class LlmResponse(BaseModel):
    step : Literal["START", "THINK", "TOOL", "OBSERVE", "OUTPUT"]
    content: Any
    tool_name: str | None
    tool_args : list[str] = []



class ApplicationStyles():
    step: Style = Style(color="Blue" , bold=True )

    content: Style = Style(color="Green" , italic=True , frame=True)

    tool: Style = Style(color="yellow" , encircle=True)

    output: Style = Style(color="cyan" , frame=True)