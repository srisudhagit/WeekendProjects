from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

class TodoItem(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the todo item")
    title: str = Field(..., description="Title of the todo item")
    description: Optional[str] = Field(None, description="Detailed description of the todo item")
    completed: bool = Field(False, description="Status of the todo item")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the todo item was created")
    due_date: Optional[datetime] = Field(None, description="Due date for the todo item")
    
class TodoList(BaseModel):
    items: List[TodoItem] = Field(default_factory=list, description="List of todo items")
    
    def add_item(self, item: TodoItem):
        self.items.append(item)
        
    def remove_item(self, item_id: UUID):
        self.items = [item for item in self.items if item.id != item_id]
        
    def get_item(self, item_id: UUID) -> Optional[TodoItem]:
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def mark_completed(self, item_id: UUID):
        item = self.get_item(item_id)
        if item:
            item.completed = True
            
    
    