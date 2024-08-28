# cyclingcalculator

Script to estimate the minimal number of calories burned while cycling. The
assumptions are chosen conservatively, meaning that the actual number of
calories burned is likely greater than the estimate.

## Installation

Clone the repository and set your current working directory to the root of the
repository, e.g., where the `pyproject.toml` file is located. Then, run the
following command:

```
pip install .
```

No dependencies except the python standard library are required. 

## Usage

The script must be executed from the command line. It is available as: `cc`,
`cycling`, and `cyclingcalculator`. To get more information, run:

```
cyclingcalculator --help
```

## Validation

The following assumptions are made:

- Wind speed is 0 m/s
- No drafting behind other cyclists.
- A constant speed is maintained throughout the ride.

A rough check to demonstrate the validity is by comparing it to the following
site:

- [gribble](https://www.gribble.org/cycling/power_v_speed.html?units=metric&rp_wr=70&rp_wb=10&rp_a=0.62&rp_cd=0.63&rp_dtl=2&ep_crr=0.003&ep_rho=1.293&ep_g=0&ep_headwind=0&p2v=200&v2p=30)

where the same parameters are used as in this script. For a 80 kg cyclist + bike
that cycles 30 km in 1 hour, you get: "If you want to ride at groundspeed
velocity 30 km/h, you must apply 169.13 watts of power." So, in 1 hour, with an
efficiency of 0.25, the energy consumption per hour is:

```
(169.13 W * 3600 s) / 0.25 = 2435472 J = 2435 kJ
```

where 2435 kJ is equal to 581 kcal.

If we run the following command:

```
cycling 80 30 1
```

results is:

```
Energy consumption human:
    - Total:                 2432 kJ / 581 kcal
Average power on the pedals:
    - Total:                 169 W
```

which is the same as the website.
