from pydantic import BaseModel, Field

# from heaan_sdk import HEFrame


class Similarity(BaseModel):
    index: int
    score: float


class EncryptedSimilarity(BaseModel):
    index: int
    # score: HEFrame = Field(default_factory=HEFrame())

    class Config:
        arbitrary_types_allowed = True
