def format_duration(duration: float) -> str:
    """Format a duration in seconds to an "hours:minutes:seconds" format."""
    minutes = int(duration // 60)
    hours = int(minutes // 60)
    if hours == 0:
        hours = None
    minutes = int(minutes % 60)
    seconds = int(duration % 60)

    if hours and hours < 10:
        hours = f"0{hours}"
    if minutes < 10:
        minutes = f"0{minutes}"
    if seconds < 10:
        seconds = f"0{seconds}"

    if hours:
        hours = f"{hours}:"
    else:
        hours = ""
    formatted_duration = f"{hours}{minutes}:{seconds}"
    return formatted_duration
