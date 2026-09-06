from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable


class ToolRegistry:
    _tools: Dict[str, ToolDefinition] = {}

    @classmethod
    def register(cls, name: str, description: str, parameters: Dict[str, Any]):
        def decorator(func: Callable):
            cls._tools[name] = ToolDefinition(
                name=name,
                description=description,
                parameters=parameters,
                handler=func,
            )
            return func
        return decorator

    @classmethod
    def get_tool(cls, name: str) -> Optional[ToolDefinition]:
        return cls._tools.get(name)

    @classmethod
    def list_tools(cls) -> List[ToolDefinition]:
        return list(cls._tools.values())

    @classmethod
    def get_openai_tool_specs(cls, enabled_tools: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        specs = []
        for name, tool in cls._tools.items():
            if enabled_tools is not None and name not in enabled_tools:
                continue
            specs.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                }
            })
        return specs
