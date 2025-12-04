from dataclasses import dataclass

@dataclass
class Domain:
  pressure: str | None = None
  visibility: str | None = None
  tankFull: str | None = None  
  temperature: str | None = None
  can_dive: str | None = None