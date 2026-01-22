
# import re
# from datetime import datetime

# MONTHS = {
#     "jan": 1, "feb": 2, "mar": 3, "apr": 4,
#     "may": 5, "jun": 6, "jul": 7, "aug": 8,
#     "sep": 9, "oct": 10, "nov": 11, "dec": 12
# }

# def parse_date(token):
#     token = token.lower()
#     if token in ["present", "current", "now"]:
#         return datetime.now()

#     parts = token.split()
#     if len(parts) == 2:
#         month = MONTHS.get(parts[0][:3], 1)
#         year = int(parts[1])
#         return datetime(year, month, 1)

#     return None


# def extract_date_ranges(text):
#     """
#     Matches:
#     Jan 2021 - Jun 2024
#     2020 - 2023
#     Feb 2022 – Present
#     """
#     pattern = r"((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s?\d{4})\s*(?:-|–|to)\s*(present|current|\w+\s?\d{4})"
#     matches = re.findall(pattern, text.lower())

#     ranges = []
#     for start, end in matches:
#         start_date = parse_date(start.strip())
#         end_date = parse_date(end.strip())
#         if start_date and end_date:
#             ranges.append((start_date, end_date))

#     return ranges


# def calculate_experience(text):
#     ranges = extract_date_ranges(text)
#     if not ranges:
#         return 0.0

#     total_months = 0
#     for start, end in ranges:
#         months = (end.year - start.year) * 12 + (end.month - start.month)
#         total_months += max(months, 0)

#     years = round(total_months / 12, 1)
#     return years


# def experience_level(years):
#     """
#     Industry-aligned experience levels
#     """
#     if years < 1:
#         return "Fresher"
#     elif years < 3:
#         return "Junior"
#     elif years < 6:
#         return "Mid"
#     elif years < 10:
#         return "Senior"
#     else:
#         return "Lead / Architect"
import re
from datetime import datetime

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "may": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12
}

def parse_date(token):
    token = token.lower().strip()

    if token in ["present", "current", "now"]:
        return datetime.now()

    # ✅ ADD: handle MM/YYYY (09/2015)
    if "/" in token:
        parts = token.split("/")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return datetime(int(parts[1]), int(parts[0]), 1)

    parts = token.split()
    if len(parts) == 2:
        month = MONTHS.get(parts[0][:3], 1)
        year = int(parts[1])
        return datetime(year, month, 1)

    return None


def extract_date_ranges(text):
    """
    Matches:
    Jan 2021 - Jun 2024
    2020 - 2023
    Feb 2022 – Present
    09/2015 to 05/2019  ✅
    """
    pattern = (
        r"((?:\d{1,2}/\d{4}|"      # MM/YYYY
        r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s?\d{4}))"
        r"\s*(?:-|–|to)\s*"
        r"(present|current|\d{1,2}/\d{4}|\w+\s?\d{4})"
    )

    matches = re.findall(pattern, text.lower())

    ranges = []
    for start, end in matches:
        start_date = parse_date(start.strip())
        end_date = parse_date(end.strip())
        if start_date and end_date:
            ranges.append((start_date, end_date))

    return ranges


def calculate_experience(text):
    ranges = extract_date_ranges(text)
    if not ranges:
        return 0.0

    total_months = 0
    for start, end in ranges:
        months = (end.year - start.year) * 12 + (end.month - start.month)
        total_months += max(months, 0)

    return round(total_months / 12, 1)


def experience_level(years):
    if years < 1:
        return "Fresher"
    elif years < 3:
        return "Junior"
    elif years < 6:
        return "Mid"
    elif years < 10:
        return "Senior"
    else:
        return "Lead / Architect"
