def detect_tone(message: str) -> str:
    s = message.lower()
    if any(x in s for x in ["angry", "frustrated", "annoyed", "stupid", "not working", "failed"]):
        return "frustrated"
    if any(x in s for x in ["sad", "upset", "lonely", "worried", "scared"]):
        return "low"
    if any(x in s for x in ["confused", "don't understand", "dont understand", "what does"]):
        return "confused"
    if any(x in s for x in ["thanks", "thank you", "awesome", "great", "happy"]):
        return "positive"
    return "neutral"

def style_instruction(tone: str) -> str:
    styles = {
      "frustrated": "The user may be frustrated. Be calm, patient, non-judgmental, and give one practical next step.",
      "low": "The user may be having a hard time. Be kind and grounded; do not overstate intimacy or claim human feelings.",
      "confused": "Explain in simple steps, define unfamiliar terms, and avoid overwhelming detail.",
      "positive": "Respond warmly and acknowledge the positive moment without excessive flattery.",
      "neutral": "Be clear, useful, and natural."
    }
    return styles[tone]
