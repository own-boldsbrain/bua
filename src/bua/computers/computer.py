from typing import Protocol, List, Literal, Dict, TypedDict, runtime_checkable

from bua.computers.actions import BaseAction


class DomTreeDict(TypedDict):
    type: str
    text: str
    tagName: str | None
    xpath: str | None
    attributes: dict[str, str]
    isVisible: bool
    isInteractive: bool
    isTopElement: bool
    isEditable: bool
    highlightIndex: int | None
    shadowRoot: bool
    children: list["DomTreeDict"]


@runtime_checkable
class Computer(Protocol):
    """Defines the 'shape' (methods/properties) our loop expects."""

    def get_environment(self) -> Literal["windows", "mac", "linux", "browser"]: ...

    def get_dimensions(self) -> tuple[int, int]: ...

    def screenshot(self) -> str: ...

    def click(self, x: int, y: int, button: str = "left") -> None: ...

    def double_click(self, x: int, y: int) -> None: ...

    def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None: ...

    def type(self, text: str) -> None: ...

    def wait(self, ms: int = 1000) -> None: ...

    def move(self, x: int, y: int) -> None: ...

    def keypress(self, keys: List[str]) -> None: ...

    def drag(self, path: List[Dict[str, int]]) -> None: ...

    def get_current_url(self) -> str: ...


@runtime_checkable
class Browser(Protocol):
    """Defines the 'shape' (methods/properties) our loop expects."""

    def screenshot(self) -> str: ...

    def dom(self) -> DomTreeDict: ...

    def get_current_url(self) -> str: ...

    def execute_action(self, action: BaseAction) -> None: ...

