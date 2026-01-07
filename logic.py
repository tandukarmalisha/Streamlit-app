import re
import pandas as pd
from typing import Any, Tuple

def format_name(name: Any) -> str:
    if not name or pd.isna(name): return "Unknown"
    return str(name).strip().title()


def clean_mobile(mobile_val: Any) -> str:
    """Extracts last 10 digits from right to left."""
    digits: str = re.sub(r'\D', '', str(mobile_val))
    if len(digits) < 10:
        raise ValueError(f"Mobile number too short: {digits}")
    return digits[-10:]
# def clean_mobile(mobile_val):
#     # 1. Handle actual Nulls
#     if pd.isna(mobile_val) or mobile_val is None:
#         return None
    
#     # 2. Handle numbers stored as floats (removes the .0)
#     if isinstance(mobile_val, float):
#         mobile_val = f"{mobile_val:.0f}"
    
#     # 3. Strip all non-digits
#     digits = re.sub(r'\D', '', str(mobile_val))
    
#     # 4. Handle empty strings
#     if not digits:
#         return None

#     # 5. Handle Nepal Prefix
#     if digits.startswith('977') and len(digits) == 13:
#         digits = digits[3:]
        
#     # 6. Final Check
#     if len(digits) != 10:
#         raise ValueError(f"Found {len(digits)} digits: ({digits})")
        
#     return digits

def split_email_data(email: Any) -> Tuple[str, str]:
    email_str = str(email).strip().lower()
    if '@' in email_str:
        return email_str.split('@', 1)
    return email_str, "unknown.com"