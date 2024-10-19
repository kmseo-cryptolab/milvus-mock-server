"""
app.schemas.base.py
"""

from pydantic import ConfigDict, BaseModel


def camel_case_alias_generator(s: str) -> str:
    """
    Converts snake_case string to camelCase.

    This function is used as an alias generator for Pydantic models,
    allowing the use of snake_case in Python while exposing camelCase in JSON.

    Parameters:
    s (str): A snake_case string (e.g., "user_name")

    Returns:
    str: A camelCase string (e.g., "userName")

    Example:
    >>> camel_case_alias_generator("user_first_name")
    "userFirstName"
    """
    return "".join(
        word.capitalize() if i > 0 else word for i, word in enumerate(s.split("_"))
    )


class BaseSchema(BaseModel):

    model_config = ConfigDict(alias_generator=camel_case_alias_generator)
