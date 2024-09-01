def j2kj(joules: float) -> float:
    """
    Return the energy in Joules as kilojoules.

    Arguments:
    ---------
        joules: the energy in Joules

    Returns:
    -------
        the energy in kilojoules

    """
    return joules / 1000


def j2kcal(joules: float) -> float:
    """
    Return the energy in Joules as kcal.

    Arguments:
    ---------
        joules: the energy in Joules

    Returns:
    -------
        the energy in kcal

    """
    return joules / 4184
