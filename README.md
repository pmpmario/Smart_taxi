The Smart Taxi Bill Summarizer is an internal automation tool designed to simplify and speed up the process of handling taxi bill submissions.
It uses OCR, Local LLM (Gemma3 via Ollama), and auto-classification logic to extract structured data from taxi receipts in a secure, offline environment.
The goal is to reduce manual workload, improve accuracy, and standardize submissions the staff

# Architecture Overview

project/
│-- app.py                         # Main Streamlit interface
│-- data/staff_data.json           # Staff name → Staff ID mapping
│
└── core/
     ├── ocr.py                    # EasyOCR extraction
     ├── llm.py                    # LLM prompt + auto-format detection
     ├── utils.py                  # Helper functions (time clean, amount clean)
     └── save_files.py             # File/folder creation and saving
     stafftaxiclaim/
     └── <staff_id>/
          └── <YYYY-MM>/
               ├── images/            # Original screenshots uploaded
               ├── ocr/               # Extracted OCR text files
               └── summary/           # LLM JSON summaries + cleaned output


Staff Name	Staff No	Date	Pick Up Time	Pick Up Location	Drop Off Time	Drop Off Location	Total Amount	

# Requirements:
Python 3.13(latest)
streamlit
easyocr
pandas
numpy
pillow
requests

# Manual taxi bill processing today involves:
Reading each receipt manually
Typing date, time, amount, pickup/drop location
Identifying shift codes manually
Saving screenshots and records separately
Significant time consumption each month

# Solution:
When accessing from Company PC it detects the staff id automatically from staff list.
Uploads multiple receipts at once in the format (jpg/png).
Automatically extracts text using OCR
Using EasyOCR (GPU optional).
Runs the text through local LLM
Gemma3 model extracts:
Date, Pick-up Time, Pick-up Location, Drop-off Time, Drop-off Location, Total Amount, Taxi provider type (Careem, Bolt, RTA/Hala)
Auto-detects shift codes - Based on pick-up time and our shift master data.
Allows editing before final save
Generates a master CSV for each staff ID per month
Stored in a structured folder hierarchy:
stafftaxiclaim/<staff_id>/<YYYY-MM>/{images, ocr, summary}


# Technical Flow:
Upload → OCR Layer
OCR Text → LLM Extraction Layer
LLM Output → Normalization Layer
Shift Detection → Business Logic Layer
Review Screen → Human Validation
Save → CSV + Audit Folder

# Why Local LLM Instead of Online APIs:
No data leaves company network
Zero cost per request
No dependency on API outages
Fast offline processing
Aligns with privacy/security best practices

# Key Features:
Unified Streamlit page
Staff auto-login and fallback dropdown
 Dynamic month-based folder generation
 OCR → LLM → Structured JSON
Auto taxi format detection (Careem, Bolt, RTA/Hala)
Shift code detection
 Editable table before saving
Master CSV auto-updating
 File saving for audit (image, ocr, summary)


