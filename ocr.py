import re

def detect_format(text):
    t = text.lower()

    if "careem" in t or "ride to" in t:
        return "CAREEM"
    if "uber" in t or "your fare" in t:
        return "UBER"
    if "bolt" in t or "payment method" in t:
        return "BOLT"
    if "dubai taxi" in t or "rta" in t:
        return "RTA_TAXI"

    return "GENERIC"


def extract_common_fields(text):
    fields = {}

    # ---- DATE ----
    date_regex = r"(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})"
    match = re.search(date_regex, text)
    fields["Date"] = match.group(1) if match else ""

    # ---- PICKUP TIME ----
    pickup_regex = r"(?:pick ?up|start|begin).*?(\d{1,2}[:\.]\d{2})"
    match = re.search(pickup_regex, text, flags=re.IGNORECASE)
    fields["Pick Up Time"] = match.group(1).replace(".", ":") if match else ""

    # ---- DROP TIME ----
    drop_regex = r"(?:drop ?off|end|finish).*?(\d{1,2}[:\.]\d{2})"
    match = re.search(drop_regex, text, flags=re.IGNORECASE)
    fields["Drop Off Time"] = match.group(1).replace(".", ":") if match else ""

    # ---- TOTAL AMOUNT ----
    amount_regex = r"(?:total|amount).*?(\d+\.\d{2}|\d+)"
    match = re.search(amount_regex, text, flags=re.IGNORECASE)
    fields["Total Amount"] = match.group(1) if match else ""

    # ---- PAYMENT METHOD ----
    pay_regex = r"(cash|visa|mastercard|apple pay|careem pay|card)"
    match = re.search(pay_regex, text, flags=re.IGNORECASE)
    fields["Payment Method"] = match.group(1).title() if match else ""

    return fields


def parse_careem(text):
    fields = extract_common_fields(text)

    # Drop Off Location
    m = re.search(r"ride to (.+?) (\d{1,2}[:\.]\d{2})", text, re.IGNORECASE)
    if m:
        fields["Drop Off Location"] = m.group(1).strip()
        fields["Drop Off Time"] = m.group(2).replace(".", ":")

    # Pickup Location (first line with pickup keyword)
    m = re.search(r"(?:from|pickup|pick up)\s+(.+)", text, re.IGNORECASE)
    fields["Pick Up Location"] = m.group(1).strip() if m else ""

    return fields


def parse_uber(text):
    fields = extract_common_fields(text)

    # Uber pickup
    m = re.search(r"pickup\s*:\s*(.+)", text, re.IGNORECASE)
    fields["Pick Up Location"] = m.group(1).strip() if m else ""

    # Uber drop
    m = re.search(r"dropoff\s*:\s*(.+)", text, re.IGNORECASE)
    fields["Drop Off Location"] = m.group(1).strip() if m else ""

    return fields


def parse_bolt(text):
    fields = extract_common_fields(text)

    # Pickup
    m = re.search(r"pickup address[:\-]\s*(.+)", text, re.IGNORECASE)
    fields["Pick Up Location"] = m.group(1).strip() if m else ""

    # Dropoff
    m = re.search(r"destination[:\-]\s*(.+)", text, re.IGNORECASE)
    fields["Drop Off Location"] = m.group(1).strip() if m else ""

    return fields


def parse_rta(text):
    fields = extract_common_fields(text)

    # Pickup: often listed as meter start
    m = re.search(r"start\s*:\s*(.+?)\s*(\d{1,2}[:\.]\d{2})", text, re.IGNORECASE)
    if m:
        fields["Pick Up Location"] = m.group(1).strip()
        fields["Pick Up Time"] = m.group(2).replace(".", ":")

    # Drop: meter end
    m = re.search(r"end\s*:\s*(.+?)\s*(\d{1,2}[:\.]\d{2})", text, re.IGNORECASE)
    if m:
        fields["Drop Off Location"] = m.group(1).strip()
        fields["Drop Off Time"] = m.group(2).replace(".", ":")

    return fields


def parse_generic(text):
    fields = extract_common_fields(text)

    # First line with any address-like pattern
    addr_regex = r"([A-Za-z0-9 ,\-]+(?:street|st|road|rd|area|city))"
    m = re.search(addr_regex, text, re.IGNORECASE)
    if m:
        fields["Pick Up Location"] = m.group(1)

    return fields


def parse_ocr_text(text):
    text_clean = text.replace("\n", " ")

    fmt = detect_format(text_clean)

    if fmt == "CAREEM":
        return parse_careem(text_clean)
    elif fmt == "UBER":
        return parse_uber(text_clean)
    elif fmt == "BOLT":
        return parse_bolt(text_clean)
    elif fmt == "RTA_TAXI":
        return parse_rta(text_clean)
    else:
        return parse_generic(text_clean)


