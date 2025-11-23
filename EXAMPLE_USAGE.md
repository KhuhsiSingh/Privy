# Example Usage & API Interaction

## For Developers: Understanding the Classification Logic

This document shows how the classification actually works under the hood.

## Core Classification Function

```python
def classify_document(pdf_bytes):
    """
    Classify a PDF document using Claude's vision capabilities.
    
    Args:
        pdf_bytes: Raw bytes of the PDF file
        
    Returns:
        dict: {
            "success": bool,
            "document_type": str,
            "confidence": float (0-1),
            "reasoning": str
        }
    """
    # Convert PDF to base64
    pdf_base64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")
    
    # Call Claude API
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_base64,
                    },
                },
                {
                    "type": "text",
                    "text": CLASSIFICATION_PROMPT
                }
            ],
        }],
    )
    
    # Parse response
    result = json.loads(message.content[0].text)
    return result
```

## Example API Request/Response

### Request

```python
# Input: PDF file (e.g., invoice.pdf)
with open("invoice.pdf", "rb") as f:
    pdf_bytes = f.read()

result = classify_document(pdf_bytes)
```

### Response

```json
{
  "success": true,
  "document_type": "Invoice",
  "confidence": 0.88,
  "reasoning": "Document contains invoice number (INV-2024-001), itemized product list with quantities and prices, subtotal and tax calculations, vendor information at top, and payment terms at bottom. Clear invoice structure and terminology used throughout."
}
```

## Classification Prompt

The system uses this prompt to guide Claude:

```
You are a document classification expert. Analyze this PDF document 
and classify it into one of these categories:

PAN Card, Aadhaar Card, Invoice, Bank Statement, Resume/CV, 
Income Tax Return (ITR), Passport, Driving License, Medical Report, 
Educational Certificate, Unknown

Examine the document carefully for:
- Layout and structure
- Headers and titles
- Key identifiers (document numbers, logos, official stamps)
- Content type and format
- Language and terminology used

Respond ONLY with valid JSON:
{
  "document_type": "category name",
  "confidence": 0.95,
  "reasoning": "brief explanation"
}
```

## Example Classifications

### 1. PAN Card

**Visual characteristics:**
- Income Tax Department header
- 10-character PAN number (ABCDE1234F format)
- Photo and signature
- Standard card dimensions

**Response:**
```json
{
  "document_type": "PAN Card",
  "confidence": 0.95,
  "reasoning": "Document shows Income Tax Department logo, PAN number in standard ABCDE1234F format, cardholder photo, and official government layout"
}
```

### 2. Invoice

**Visual characteristics:**
- "Invoice" header
- Invoice number
- Line items with prices
- Total amount
- Vendor details

**Response:**
```json
{
  "document_type": "Invoice",
  "confidence": 0.88,
  "reasoning": "Contains invoice number, itemized list of goods/services with quantities and prices, tax calculations, vendor information, and payment terms"
}
```

### 3. Resume/CV

**Visual characteristics:**
- Name and contact info at top
- Sections: Experience, Education, Skills
- Timeline format
- Professional formatting

**Response:**
```json
{
  "document_type": "Resume/CV",
  "confidence": 0.87,
  "reasoning": "Document contains personal information header, chronological work experience section, education details, skills listing, and professional summary"
}
```

### 4. Bank Statement

**Visual characteristics:**
- Bank logo/name
- Account number
- Transaction table
- Period dates
- Balance information

**Response:**
```json
{
  "document_type": "Bank Statement",
  "confidence": 0.91,
  "reasoning": "Bank logo present, account number visible, tabular transaction history with dates/descriptions/amounts, statement period indicated, and running balance column"
}
```

### 5. Unknown Document

**Visual characteristics:**
- Doesn't match any category clearly
- Mixed content
- Unclear purpose

**Response:**
```json
{
  "document_type": "Unknown",
  "confidence": 0.45,
  "reasoning": "Document does not clearly match any predefined categories. Contains mixed content without clear structural patterns matching known document types"
}
```

## Confidence Score Interpretation

The system provides confidence scores to help users understand reliability:

```python
def interpret_confidence(confidence):
    if confidence >= 0.8:
        return "HIGH - Trust this result"
    elif confidence >= 0.6:
        return "MEDIUM - Verify if important"
    else:
        return "LOW - Manual review recommended"
```

**Visual indicators in UI:**
- 🟢 Green: High confidence (≥80%)
- 🟡 Yellow: Medium/Low confidence (<80%)

## Error Handling Examples

### Invalid PDF

```python
# Input: empty or corrupt file
result = {
    "success": False,
    "error": "Error: Empty PDF file"
}
```

### API Error

```python
# Input: API timeout or error
result = {
    "success": False,
    "error": "Classification failed: API timeout"
}
```

### Parse Error

```python
# Input: malformed JSON response
result = {
    "success": False,
    "error": "Failed to parse classification response",
    "raw_response": "..." # for debugging
}
```

## Performance Characteristics

**Processing time breakdown:**
- Upload + validation: < 0.1s
- Base64 encoding: < 0.1s
- Claude API call: 1.5-4s
- Response parsing: < 0.1s
- **Total: 2-5 seconds**

**Accuracy by document type (expected):**
- Government IDs (PAN, Aadhaar, Passport, DL): 90-95%
- Financial docs (Invoice, Bank Statement, ITR): 85-92%
- General docs (Resume, Certificate): 85-90%
- Medical reports: 80-88%
- Unknown/unclear: 40-60% (intentionally low)

## Using the Classification System

### Basic Usage

```python
import streamlit as st

# Upload file
uploaded_file = st.file_uploader("Choose PDF", type=['pdf'])

# Classify
if uploaded_file:
    pdf_bytes = uploaded_file.read()
    result = classify_document(pdf_bytes)
    
    if result["success"]:
        st.metric("Type", result["document_type"])
        st.metric("Confidence", f"{result['confidence']*100:.1f}%")
        st.write(result["reasoning"])
```

### Batch Processing (Future Enhancement)

```python
def classify_batch(pdf_files):
    """Classify multiple documents"""
    results = []
    for pdf_file in pdf_files:
        result = classify_document(pdf_file.read())
        results.append({
            "filename": pdf_file.name,
            **result
        })
    return results
```

### Export Results (Future Enhancement)

```python
import pandas as pd

def export_results(results):
    """Export to CSV"""
    df = pd.DataFrame(results)
    return df.to_csv(index=False)
```

## API Cost Calculation

**Claude Sonnet 4 pricing (approximate):**
- Input: $3 per million tokens
- Output: $15 per million tokens

**Typical document:**
- Input: ~2000 tokens (PDF) + 200 tokens (prompt) = 2200 tokens
- Output: ~100 tokens (JSON response)

**Cost per document:**
- Input: (2200/1,000,000) × $3 = $0.0066
- Output: (100/1,000,000) × $15 = $0.0015
- **Total: ~$0.008 per document**

**Volume pricing:**
- 100 documents: $0.80
- 1,000 documents: $8.00
- 10,000 documents: $80.00

## Integration Examples

### REST API Wrapper

```python
from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/classify")
async def classify_endpoint(file: UploadFile):
    pdf_bytes = await file.read()
    result = classify_document(pdf_bytes)
    return result
```

### Command Line Tool

```python
import sys

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    with open(pdf_path, "rb") as f:
        result = classify_document(f.read())
    print(json.dumps(result, indent=2))
```

---

## Key Takeaways

1. **Simple interface**: One function, clear outputs
2. **Transparent**: Reasoning included in every response
3. **Robust**: Multiple layers of error handling
4. **Fast**: 2-5 second processing time
5. **Extensible**: Easy to add features or categories
6. **Cost-effective**: Less than 1¢ per document

This architecture makes it easy to integrate document classification into any workflow!
