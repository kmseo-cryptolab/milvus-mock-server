import base64

from pydantic import BaseModel, Field

# from heaan_sdk import HEFrame


class Document(BaseModel):
    pass


class EncryptedDocument(BaseModel):
    index: int
    # score: HEFrame = Field(default_factory=HEFrame())

    class Config:
        arbitrary_types_allowed = True


class DocumentDto(BaseModel):
    index: int
    document: str
    embedding: str
