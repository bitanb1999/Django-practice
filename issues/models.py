from abc import ABC, abstractmethod
from typing import override
class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass
    def to_dict(self):
        return {key:value for key,value in self.__dict__.items() if not key.startswith('_')}
class Reporter(BaseEntity):
    def __init__(self,id,name,email,team):
        self.id=id
        self.name=name
        self.email=email
        self.team=team
    def validate(self):
        if not self.name:
            raise ValueError("Reporter name cannot be empty.")
        if not self.email:
            raise ValueError("Reporter email cannot be empty.")
        if not self.team:
            raise ValueError("Reporter team cannot be empty.")
        if '@' not in self.email:
            raise ValueError("Reporter email must be a valid email address.")

class Issue(BaseEntity):
    def __init__(self,id,title,description,reporter_id,status,priority):
        self.id=id
        self.title=title
        self.description=description
        self.reporter_id=reporter_id
        self.status=status
        self.priority=priority
    def validate(self):
        if not self.title:
            raise ValueError("Issue title cannot be empty.")
        if not self.description:
            raise ValueError("Issue description cannot be empty.")
        if not self.reporter_id:
            raise ValueError("Issue reporter cannot be empty.")
        if  self.status not in ['open', 'in_progress', 'closed', 'resolved']:
            raise ValueError("Issue status is invalid.")
        if self.priority not in ['low', 'medium', 'high', 'critical']:
            raise ValueError("Issue priority is invalid.")

    def describe(self):
        return f"[{self.priority}] {self.title} — {self.description}"
    
class CriticalIssue(Issue):
    @override
    def describe(self):
        return f"[URGENT] {self.title} — needs immediate attention"
    
class LowPriorityIssue(Issue):
    @override
    def describe(self):
        return f"{self.title} — low priority, handle when free"


# Create your models here.
