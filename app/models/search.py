from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    query:str
    top_k:int = Field(default=50, ge=1, le=100)
    
    
    
    
    
    
    
    
    
    
    
    
    
    