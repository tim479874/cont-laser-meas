# cont-laser-meas

Simple python command line tool to do continous laser measurements with the Laser Technology TruePulse 360b Rangefinder via Bluetooth.

## Dependencies

Python 3.x

Modules:
- pyserial
- time
- csv
- os

### Workflow

1. First connect the TruePulse Rangefinder via Bluetooth. 
2. Find the Serial Port it is connected to(Windows: COMX, Linux: /dev/rfcommX e.g.)
3. Start the command line tool and choose your settings. 
4. Then take your measurements.
