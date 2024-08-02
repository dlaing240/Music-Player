def format_duration(duration: float) -> str:
    """
    Formats a duration in seconds to a "minutes:seconds" format

    Parameters
    ----------
    duration

    Returns
    -------

    """
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    if seconds < 10:
        seconds = f"0{seconds}"
    formatted_duration = f"{minutes}:{seconds}"
    return formatted_duration
