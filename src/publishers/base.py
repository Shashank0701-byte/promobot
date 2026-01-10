# src/publishers/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePublisher(ABC):
    """
    The Abstract Base Class (Interface) that all publishers must follow.
    This ensures consistency across Dev.to, Reddit, etc.
    """

    @abstractmethod
    def publish(self, content: Dict[str, Any]) -> str:
        """
        Publishes content to the platform.
        
        Args:
            content: A dictionary containing 'title', 'body', 'tags', etc.
            
        Returns:
            str: The URL of the published post or draft.
        """
        pass