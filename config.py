"""
Wayne AI Pharma - Configuration & Constants
"""
import os

# App
APP_NAME = "Wayne AI Pharma"
APP_ICON = "🧬"
APP_VERSION = "1.0.0"

# Brand Colors
PRIMARY_COLOR = "#2563eb"
PRIMARY_LIGHT = "#3b82f6"
PRIMARY_DARK = "#1d4ed8"
SUCCESS_COLOR = "#10b981"
WARNING_COLOR = "#f59e0b"
DANGER_COLOR = "#ef4444"
BG_COLOR = "#ffffff"
TEXT_COLOR = "#111827"
TEXT_MUTED = "#6b7280"

# Database
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wayne_pharma.db")

# AI Model (Codex / OpenAI-compatible)
AI_MODEL = "gpt-4o"

# African regulatory bodies
REGULATORY_BODIES = {
    "Kenya": "PPB (Pharmacy and Poisons Board)",
    "Nigeria": "NAFDAC (National Agency for Food and Drug Administration and Control)",
    "South Africa": "SAHPRA (South African Health Products Regulatory Authority)",
    "Egypt": "EDA (Egyptian Drug Authority)",
    "Ghana": "FDA Ghana",
    "Tanzania": "TMDA (Tanzania Medicines and Medical Devices Authority)",
    "Uganda": "NDA (National Drug Authority)",
    "Ethiopia": "EFDA (Ethiopian Food and Drug Authority)",
}

# African countries for recruitment analysis
AFRICAN_COUNTRIES = [
    "Kenya", "Nigeria", "South Africa", "Egypt", "Ghana",
    "Tanzania", "Uganda", "Ethiopia", "Morocco", "Rwanda"
]

# McKinsey comparison benchmarks
MCKINSEY_AVG_TIMELINE_MONTHS = 18
MCKINSEY_AVG_COST_MILLIONS = 4.2

# PHI regex patterns for redaction
PHI_PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone": r'\b(\+?\d{1,4}[\s.-]?)?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,9}\b',
    "name_patterns": [
        r'\b(?:Dr\.|Mr\.|Mrs\.|Ms\.|Prof\.)\s+[A-Z][a-z]+\b',
        r'Patient(?:\s+Name)?:\s*[A-Za-z\s]+',
        r'Name:\s*[A-Za-z\s]+',
    ]
}

# Maximum file size (15MB)
MAX_FILE_SIZE_MB = 15
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Supported file types
SUPPORTED_TYPES = ["pdf", "docx"]

# Auto-delete grace period in days
DATA_RETENTION_DAYS = 90
