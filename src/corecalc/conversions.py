from datetime import datetime


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

def datetime2seconds(dt: datetime) -> float:
    """
    Return the datetime as seconds.

    Arguments:
    ---------
        dt: the datetime

    Returns:
    -------
        the datetime as seconds

    """
    return dt.hour * 3600 + dt.minute * 60 + dt.second

