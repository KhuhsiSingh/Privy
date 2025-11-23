# 🚀 QUICK START GUIDE - Document Classification Portal

## For Reviewers: Deploy in 5 Minutes

### Option 1: Deploy to Streamlit Cloud (Recommended)

1. **Get API Key** (30 seconds)
   - Go to console.anthropic.com
   - Create free account / log in
   - Generate API key

2. **Deploy** (2 minutes)
   - Go to share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select repository or paste GitHub URL
   - Main file: `app.py`
   
3. **Configure** (1 minute)
   - In app settings → Secrets
   - Add:
     ```
     ANTHROPIC_API_KEY = "your-key-here"
     ```

4. **Launch** (1 minute)
   - Click "Deploy"
   - Wait for build
   - 🎉 App is live!

### Option 2: Run Locally (3 Minutes)

```bash
# Install
pip install streamlit anthropic

# Set API key
export ANTHROPIC_API_KEY='your-key-here'

# Run
streamlit run app.py
```

Open: http://localhost:8501

## Testing the App

1. Upload any PDF (sample invoice, resume, ID card, etc.)
2. Click "Classify Document"
3. View results:
   - Document type
   - Confidence score
   - Classification reasoning

## What to Test

✅ Upload a digital PDF (e.g., downloaded invoice)
✅ Upload a scanned PDF (e.g., photo of ID card)
✅ Try uploading non-PDF file (should show error)
✅ Try uploading corrupt/empty PDF (should handle gracefully)
✅ Check confidence scores and reasoning
✅ Test different document types

## Architecture at a Glance

```
PDF Upload → Validation → Claude Sonnet 4 → Results
                                ↓
                    (Native OCR + Classification)
```

## Key Features

- 🔍 11 document categories + Unknown fallback
- 📊 Confidence scoring (0-100%)
- 🧠 AI reasoning explanation
- ⚡ 2-5 second processing
- 🔒 Secure (no data storage)
- 📱 Mobile friendly

## Files Overview

- **app.py** - Main application (200 lines)
- **README.md** - Full documentation
- **DEPLOYMENT.md** - Deployment instructions
- **PROJECT_SUMMARY.md** - Detailed project overview
- **requirements.txt** - Dependencies (just 2!)
- **test_classification.py** - Demo test suite

## Expected Accuracy

- High confidence (≥80%): ~90% of well-formatted docs
- Works on both scanned and digital PDFs
- "Unknown" fallback for unclear documents

## Supported Document Types

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
11. Unknown

## Extensibility

**Adding new category:**
```python
# In app.py, line 11:
DOCUMENT_CATEGORIES = [
    # ... existing categories
    "New Category Name",  # Just add here!
]
```

No retraining needed! Prompt adapts automatically.

## Tech Stack

- **Frontend**: Streamlit
- **AI**: Claude Sonnet 4 (via Anthropic API)
- **OCR**: Built into Claude's PDF processing
- **Deployment**: Streamlit Cloud / Hugging Face / Railway

## Cost Estimate

- Anthropic API: ~$0.003 per document (1000 docs = $3)
- Streamlit Cloud: FREE
- Total hosting: FREE tier available

## Support

- Questions about Anthropic API: console.anthropic.com/docs
- Questions about Streamlit: docs.streamlit.io
- Deploy issues: Check DEPLOYMENT.md

---

**🎯 Bottom Line**: Upload to GitHub → Deploy on Streamlit Cloud → Add API key → Done!

**⏱️ Time to live demo: < 10 minutes**
