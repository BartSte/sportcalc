from corecalc.stats import MetsSpeedStats


class SpeedSkatingStats(MetsSpeedStats):
    """
    Statistics for a walking exercise.

    - source:
        https://cdn-links.lww.com/permalink/mss/a/mss_43_8_2011_06_13_ainsworth_202093_sdc1.pdf

    I combined the roller blading, ice skating and speed skating values:
        - Ice skating requires 5.5 METs at 14.48 km/h,
        - Roller blading requires 7.5 METs at 14.48 km/h.
        - Roller blading requires 9.8 METs at 17.7 km/h.
        - Assume that "ice skating" is the same at low speeds as "speed skating".
        - Assume that ice skating scaler linearly with roller blading, I assumed
          that the speed skating values is 7.8 METs and 17.7 km/h.
        - Doing the same for roller blading at 21.0 km/h (12.3 METs) which is
          10.3 METs for speed skating.
        - Doing the same for roller blading at 24.0 km/h (14.0 METs) which is
          12.0 METs for speed skating.
        - Competitive speed skating is has a METs value of 13.3 METs, which is
          can be interpolated to

        Roller blading (from the source above)
        | Speed (km/h) | METs |
        |--------------|------|
        | 14.48        | 7.5  |
        | 17.7         | 9.8  |
        | 21.0         | 12.3 |
        | 24.0         | 14.0 |

        Speed skating (assumed based on roller blading)
        | Speed (km/h) | METs |
        |--------------|------|
        | 14.48        | 5.5  |
        | 17.7         | 7.8  |
        | 21.0         | 10.3 |
        | 24.0         | 12.0 |
        | 26.6         | 13.3 |

    METS_KCAL_KG_H = 5.5, 7.8, 10.3, 12.0, 13.3
    METS_KM_H = 14.48, 17.7, 21.0, 24.0, 26.6

    Still not ready comfortable with these numbers. For example, when doing 1
    lap in 1 minute (24 km/h) the METs value is 12.0. This is similar to
    running with a speed of 12 km/h and a METs value of 12.0. For me it feels
    that running is more intense than skating at theses speeds...
    """
    METS_KCAL_KG_H = 5.5, 7.8, 10.3, 12.0, 13.3
    METS_KM_H = 14.48, 17.7, 21.0, 24.0, 26.6

