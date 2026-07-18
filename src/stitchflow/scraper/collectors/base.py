from abc import ABC, abstractmethod
from typing import List
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import TrendSignal


class BaseCollector(ABC):
    """Every collector must implement collect() -> List[TrendSignal].

    This is the only contract the Fusion Engine depends on, so adding a
    new source later (Pinterest, TikTok Creative Center, etc.) means
    writing one new class here and nothing else changes downstream.
    """

    source_name: str = "base"

    @abstractmethod
    def collect(self) -> List[TrendSignal]:
        ...
