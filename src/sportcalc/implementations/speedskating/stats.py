from sportcalc.core.stats import MetsSpeedStats


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
        - Assume that ice skating scales linearly with roller blading, I assumed
          that the speed skating values is 7.8 METs and 17.7 km/h:
            - Roller blading: 9.8 METs at 17.7 km/h minus 7.5 METs at 14.48 km/h
              is 2.3 METs for 3.22 km/h (0.71 METs per km/h).
            - 7.5 METs at 14.48 km/h plus 2.3 METs for 3.22 km/h is 9.8 METs
              at 17.7 km/h.
        - Doing the same for roller blading at 21.0 km/h (12.3 METs) which is
          10.3 METs for speed skating.
        - Doing the same for roller blading at 24.0 km/h (14.0 METs) which is
          12.0 METs for speed skating.
        - Competitive speed skating is has a METs value of 13.3 METs but the
          speed is not specified. In the point above, the METs value per km/h
          is (14.0 - 12.3) / (24.0 - 21.0) = 0.57 METs per km/h. A METs value
          of 13.3 METs would then correspond to an increase of
          (13.3 - 12.0) / 0.57 = 2.3 km/h which is 26.3 km/h.

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
        | 26.3         | 13.3 |

    METS_KCAL_KG_H = 5.5, 7.8, 10.3, 12.0, 13.3
    METS_KM_H = 14.48, 17.7, 21.0, 24.0, 26.6

    Still not ready comfortable with these numbers. For example, when doing 1
    lap in 1 minute (24 km/h) the METs value is 12.0. This is similar to
    running with a speed of 12 km/h and a METs value of 12.0. For me it feels
    that running is more intense than skating at theses speeds. I think the
    assumption that "ice skating" and "speed skating" are the same is wrong.
    Similar to riding a bike, or a racing bike.

    Riding a racing bike at 25 km/h requires about 10 METs. This should
    correspond to skating at 21 km/h this is abount 67s per round, which is
    pretty easy, but so is riding a bike at 25 km/h. These values are probably
    oke.
    """

    METS_KCAL_KG_H = 5.5, 7.8, 10.3, 12.0, 13.3
    METS_KM_H = 14.48, 17.7, 21.0, 24.0, 26.3
