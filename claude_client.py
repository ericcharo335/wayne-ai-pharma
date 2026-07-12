"""
Wayne AI Pharma - AI API Integration (Codex / OpenAI-compatible)
Sends redacted text to the LLM and parses JSON response.
"""
import json
import re
from openai import OpenAI
import streamlit as st
from config import AI_MODEL, MCKINSEY_AVG_TIMELINE_MONTHS, MCKINSEY_AVG_COST_MILLIONS, REGULATORY_BODIES


SYSTEM_PROMPT = """You are Wayne AI Pharma. The #1 clinical trial AI for Africa.

Analyze this redacted clinical trial document. Be specific to Africa. Compare to McKinsey benchmarks.

Focus on:
1. Regulatory requirements for PPB (Kenya), NAFDAC (Nigeria), SAHPRA (South Africa), EDA (Egypt)
2. African healthcare infrastructure realities
3. Realistic patient recruitment across African countries
4. Africa-specific risks (logistics, power, supply chain, political, cultural)
5. Cost advantages and challenges unique to Africa

Output STRICT valid JSON with these exact keys:
{
  "timeline": "X months" (string),
  "cost": "$X" (string, include dollar sign and commas),
  "risks": [{"risk": "Risk description", "mitigation": "How to mitigate"}],
  "compliance": {"kenya_score": 0-100, "nigeria_score": 0-100, "sa_score": 0-100, "egypt_score": 0-100, "checklist": ["item1", "item2", ...]},
  "recruitment": {"kenya": "X patients/month", "nigeria": "X patients/month", "south_africa": "X patients/month", "egypt": "X patients/month"},
  "advantage": "Concise paragraph on why Wayne AI beats McKinsey for African trials",
  "confidence": 0-100 (number)
}

Be aggressive with timelines and costs. Africa can be faster and cheaper. Do NOT wrap JSON in markdown code blocks. Output ONLY the JSON object."""


def get_client():
    api_key = st.secrets.get("CODEWX_API_KEY", "")
    if not api_key:
        raise ValueError(
            "Codex API key not found. Please set CODEWX_API_KEY in .streamlit/secrets.toml."
        )
    return OpenAI(
        api_key=api_key,
        base_url="https://api.codex.openai.com/v1"
    )


def analyze_document(redacted_text: str) -> dict:
    """
    Send redacted text to the AI model and parse JSON response.
    Returns parsed analysis dict.
    """
    client = get_client()

    # Truncate text if extremely long
    max_chars = 80000
    text_to_send = redacted_text[:max_chars]
    if len(redacted_text) > max_chars:
        text_to_send += f"\n\n[Note: Document was truncated from {len(redacted_text)} to {max_chars} characters]"

    response = client.chat.completions.create(
        model=AI_MODEL,
        max_tokens=4096,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text_to_send}
        ]
    )

    response_text = response.choices[0].message.content.strip()

    # Parse JSON from response — handle possible markdown wrapping
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
    else:
        json_str = response_text

    try:
        analysis = json.loads(json_str)
    except json.JSONDecodeError:
        # Try to fix common issues
        cleaned = re.sub(r'```json\s*|\s*```', '', response_text)
        cleaned = cleaned.strip()
        try:
            analysis = json.loads(cleaned)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse AI response as JSON. Raw response: {response_text[:500]}")

    # Validate required keys
    required_keys = ["timeline", "cost", "risks", "compliance", "recruitment", "advantage", "confidence"]
    for key in required_keys:
        if key not in analysis:
            raise ValueError(f"Missing required key in AI response: '{key}'")

    return analysis
