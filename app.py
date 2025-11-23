import streamlit as st
import anthropic
import base64
import os
from io import BytesIO
import json

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Document categories
DOCUMENT_CATEGORIES = [
    "PAN Card",
    "Aadhaar Card",
    "Invoice",
    "Bank Statement",
    "Resume/CV",
    "Income Tax Return (ITR)",
    "Passport",
    "Driving License",
    "Medical Report",
    "Educational Certificate",
    "Unknown"
]

def classify_document(pdf_bytes):
    """
    Classify a PDF document using Claude's vision capabilities.
    Returns document type and confidence score.
    """
    try:
        # Convert PDF to base64
        pdf_base64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")
        
        # Create the classification prompt
        prompt = f"""You are a document classification expert. Analyze this PDF document and classify it into one of these categories:

{', '.join(DOCUMENT_CATEGORIES)}

Examine the document carefully for:
- Layout and structure
- Headers and titles
- Key identifiers (like document numbers, logos, official stamps)
- Content type and format
- Language and terminology used

Respond ONLY with a valid JSON object in this exact format (no additional text or markdown):
{{
  "document_type": "one of the exact categories listed above",
  "confidence": 0.95,
  "reasoning": "brief explanation of why you classified it this way"
}}

IMPORTANT: 
- The confidence should be a number between 0 and 1
- Use "Unknown" if the document doesn't clearly fit any category
- Your entire response must be valid JSON only"""

        # Call Claude API with the PDF
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {
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
                            "text": prompt
                        }
                    ],
                }
            ],
        )
        
        # Parse the response
        response_text = message.content[0].text.strip()
        
        # Clean up any markdown formatting if present
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        result = json.loads(response_text)
        
        return {
            "success": True,
            "document_type": result.get("document_type", "Unknown"),
            "confidence": result.get("confidence", 0.0),
            "reasoning": result.get("reasoning", "No reasoning provided")
        }
        
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Failed to parse classification response: {str(e)}",
            "raw_response": response_text if 'response_text' in locals() else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Classification failed: {str(e)}"
        }

# Streamlit UI
st.set_page_config(
    page_title="Document Classification Portal",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Document Classification Portal")
st.markdown("""
Upload a PDF document (scanned or digital) to automatically classify it.
Supports 10+ document types including PAN, Aadhaar, invoices, bank statements, and more.
""")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=['pdf'],
    help="Upload a scanned or digital PDF document"
)

if uploaded_file is not None:
    # Display file info
    st.info(f"📎 File uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.2f} KB)")
    
    # Classify button
    if st.button("🔍 Classify Document", type="primary"):
        with st.spinner("Analyzing document..."):
            # Read PDF bytes
            pdf_bytes = uploaded_file.read()
            
            # Validate PDF
            if len(pdf_bytes) == 0:
                st.error("❌ Error: Empty PDF file")
            elif not pdf_bytes.startswith(b'%PDF'):
                st.error("❌ Error: Invalid PDF file format")
            else:
                # Classify the document
                result = classify_document(pdf_bytes)
                
                if result["success"]:
                    # Display results
                    st.success("✅ Classification Complete!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Document Type", result["document_type"])
                    with col2:
                        confidence_pct = result["confidence"] * 100
                        st.metric("Confidence", f"{confidence_pct:.1f}%")
                    
                    # Show reasoning
                    with st.expander("📝 Classification Reasoning"):
                        st.write(result["reasoning"])
                    
                    # Confidence indicator
                    if result["confidence"] >= 0.8:
                        st.success("🎯 High confidence classification")
                    elif result["confidence"] >= 0.6:
                        st.warning("⚠️ Medium confidence - please verify")
                    else:
                        st.warning("⚠️ Low confidence - manual review recommended")
                else:
                    st.error(f"❌ {result['error']}")
                    if "raw_response" in result and result["raw_response"]:
                        with st.expander("Debug Info"):
                            st.code(result["raw_response"])

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This portal uses AI to automatically classify PDF documents into categories.
    
    **Supported Document Types:**
    """)
    for category in DOCUMENT_CATEGORIES:
        st.markdown(f"- {category}")
    
    st.markdown("---")
    st.markdown("""
    **Features:**
    - ✅ Handles scanned & digital PDFs
    - ✅ OCR for scanned documents
    - ✅ Confidence scoring
    - ✅ Error handling
    """)
    
    st.markdown("---")
    st.caption("Built for Privy PM Assignment")
