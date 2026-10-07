import re

def extract_timestamps(text: str) -> list[str]:
    """Extracts all timestamp strings like [Video: 12:34] or 12:34 from text."""
    pattern = r'(?:\[Video:\s*)?(\d{1,2}:\d{2}(?::\d{2})?)(?:\s*-\s*(\d{1,2}:\d{2}(?::\d{2})?))?(?:\])?'
    matches = re.findall(pattern, text)
    timestamps = []
    for match in matches:
        if match[0]:
            timestamps.append(match[0])
    return timestamps

def time_str_to_seconds(time_str: str) -> int:
    """Converts MM:SS or HH:MM:SS to total seconds."""
    parts = list(map(int, time_str.split(':')))
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0
