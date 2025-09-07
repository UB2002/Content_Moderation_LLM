from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from config.db import get_db
from schema.moderationSchema import TextModeration, ImageModeration, ModerationResponse, Summary
from utils.text_image_classification import text_response, image_response
from models.moderation import ModerationRequest, ModerationResult
from utils.hash_content import sha256_of_upload, sha256_of_bytes
import json


router = APIRouter()

# Handle both array and single value formats from LLM
def extract_value(value):
    if isinstance(value, list) and len(value) > 0:
        return value[0]
    return value if value is not None else ""


@router.get("/")
def index():
    return {"message": "classification routes are up"}


@router.post("/text_call")
def text_classification(data: TextModeration, db: Session = Depends(get_db)):
    content_hash = sha256_of_bytes(data.text.encode())

    moderation_req = ModerationRequest(content_type="text", content_hash=content_hash, email=data.email, status="processing")
    db.add(moderation_req)
    db.commit()
    db.refresh(moderation_req)

    response = text_response(data.text)
    
    try:
        # Clean the response by removing markdown formatting
        clean_response = response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]  # Remove ```json
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]  # Remove ```
        clean_response = clean_response.strip()
        
        parsed = json.loads(clean_response)
    except Exception as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {response}")
        parsed = {
            "classification": "safe",
            "confidence": 0.99,
            "reasoning": "Error parsing LLM response",
            "llm_response": response
        }
    
    moderation_result = ModerationResult(
        request_id = moderation_req.id,
        classification = extract_value(parsed.get("classification")),
        confidence = extract_value(parsed.get("confidence")),
        reasoning = extract_value(parsed.get("reasoning")),
        llm_response = extract_value(parsed.get("llm_response"))
    )

    db.add(moderation_result)
    moderation_req.status = "completed"
    db.commit()

    return {"status": "success", "result": parsed}


@router.post("/image_call")
def image_classification(email: str = Form(...), db: Session = Depends(get_db), file: UploadFile = File(...)):
    file_hash = sha256_of_upload(file=file)
    data = ModerationRequest(content_type="image", content_hash=file_hash, email=email, status="processing")
    db.add(data)
    db.commit()
    db.refresh(data)

    response = image_response(file)
    
    try:
        # Clean the response by removing markdown formatting
        clean_response = response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]  # Remove ```json
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]  # Remove ```
        clean_response = clean_response.strip()
        
        parsed = json.loads(clean_response)
    except Exception as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {response}")
        parsed = {
            "classification": "safe",
            "confidence": 0.99,
            "reasoning": "Error parsing LLM response",
            "llm_response": response
        }
    
    moderation_result = ModerationResult(
        request_id = data.id,
        classification = extract_value(parsed.get("classification")),
        confidence = extract_value(parsed.get("confidence")),
        reasoning = extract_value(parsed.get("reasoning")),
        llm_response = extract_value(parsed.get("llm_response"))
    )

    db.add(moderation_result)
    data.status = "completed"
    db.commit()

    return {"status": "success", "result": parsed}

@router.get("/summary")
def summary(user: str, db: Session = Depends(get_db)):

    total_requests = db.query(ModerationRequest).filter(ModerationRequest.email == user).count()
    
    classification_counts = {}
    results = db.query(ModerationResult).join(ModerationRequest).filter(
        ModerationRequest.email == user
    ).all()
    

    for result in results:
        classification = result.classification
        if classification in classification_counts:
            classification_counts[classification] += 1
        else:
            classification_counts[classification] = 1
    
    return {
        "total_request": total_requests,
        "by_classification": classification_counts
    }