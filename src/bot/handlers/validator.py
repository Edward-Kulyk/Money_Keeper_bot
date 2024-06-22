from typing import Any, Callable, Coroutine, TypeVar

T = TypeVar("T", bound=Callable[..., Coroutine[Any, Any, Any]])
