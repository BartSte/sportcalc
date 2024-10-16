from datetime import datetime

from corecalc.exceptions import CoreValueError


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


def kcal2j(kcal: float) -> float:
    """
    Return the energy in kcal as Joules.

    Arguments:
    ---------
        kcal: the energy in kcal

    Returns:
    -------
        the energy in Joules

    """
    return kcal * 4184


def ms2kmh(mps: float) -> float:
    """
    Return the speed in m/s as km/h.

    Arguments:
    ---------
        mps: the speed in m/s

    Returns:
    -------
        the speed in km/h

    """
    return mps * 3.6


def datetime2seconds(dt: datetime, check: bool = False) -> float:
    """
    Return the datetime as seconds.

    Arguments:
    ---------
        dt: the datetime
        check: whether to check if the datetime is positive and non-zero
            (default: False)

    Returns:
    -------
        the datetime as seconds

    """
    result = dt.hour * 3600 + dt.minute * 60 + dt.second
    if check and result <= 0:
        raise CoreValueError(f"Invalid time: {dt}")
    else:
        return result
