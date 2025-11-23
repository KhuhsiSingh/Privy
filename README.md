# Document Classification Portal

A web-based document classification system that automatically identifies PDF document types using AI.

## 🚀 Live Demo

Deploy to Streamlit Cloud:
1. Fork/upload this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add `ANTHROPIC_API_KEY` to Streamlit secrets
5. Deploy!

## 📋 Supported Document Categories

1. PAN Card
2. Aadhaar Card
3. Invoice
4. Bank Statement
5. Resume/CV
6. Income Tax Return (ITR)
7. Passport
8. Driving License
9. Medical Report
10. Educational Certificate
11. Unknown (fallback category)

## 🏗️ Technical Approach

**Architecture:**
- **Frontend:** Streamlit for simple, interactive UI
- **Classification Engine:** Claude Sonnet 4 with native PDF processing
- **OCR:** Built-in via Claude's multimodal capabilities (handles both scanned & digital PDFs)

**How it works:**
1. User uploads a PDF (scanned or digital)
2. PDF is validated and converted to base64
3. Claude analyzes the document using vision capabilities
4. Returns predicted type + confidence (0-1 scale) + reasoning
5. Results displayed with confidence indicators

**Key Features:**
- ✅ Native PDF processing (no external OCR needed)
- ✅ Handles both scanned and digital documents
- ✅ Confidence scoring with visual indicators
- ✅ Error handling for invalid/empty PDFs
- ✅ Clean, user-friendly interface

## 💻 Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Run the app
streamlit run app.py
```

## 🎯 Accuracy & Performance

- **Confidence Thresholds:**
  - High (≥80%): Green indicator
  - Medium (60-79%): Yellow warning
  - Low (<60%): Manual review recommended

- **Expected Accuracy:** ~85-95% on well-formatted documents
- **Processing Time:** 2-5 seconds per document

## 🔧 Extensibility

**Adding New Categories:**
1. Add category name to `DOCUMENT_CATEGORIES` list in `app.py`
2. No retraining needed - prompt-based classification adapts automatically
3. For specialized domains, enhance the prompt with specific identifiers

**Future Enhancements:**
- Batch processing for multiple documents
- Export classification results to CSV/JSON
- Document preview/thumbnail
- Multi-language support
- Custom category configuration via UI
- Integration with document management systems
- Fine-tuned models for specific document types

## 📊 Error Handling

- Empty PDF validation
- File format verification (checks PDF header)
- JSON parsing error handling
- API error handling with user-friendly messages
- Debug mode for troubleshooting

## 🔐 Security Notes

- API key stored in environment variables/secrets
- No document storage - processed in memory only
- Files not persisted after classification

---

**Built for:** Privy PM Assignment  
**Tech Stack:** Streamlit + Claude Sonnet 4  
**Deployment:** Streamlit Cloud (recommended) or any Python hosting platform
