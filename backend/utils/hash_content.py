import hashlib
from fastapi import UploadFile

def sha256_of_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_of_upload(file: UploadFile) -> str:
    h = hashlib.sha256()
    for chunk in iter(lambda: file.file.read(8192), b""):
        h.update(chunk)
    file.file.seek(0)
    return h.hexdigest()