def correctBandwidth(f1, f2):
    """Checks whether measured bandwidth is in approximity of theoretical dab+ bandwidth."""
    theory = 1536000    # [Hz]
    delta = 5000        # [Hz]

    global frekvencie
    measured = frekvencie[f2] - frekvencie[f1]

    if (theory-delta < measured < theory+delta):
        return True
    else:
        return False
    pass
