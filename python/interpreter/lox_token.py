from dataclasses import dataclass
from typing import Optional

from token_type import TokenType


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: Optional[str]
    line: int

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
