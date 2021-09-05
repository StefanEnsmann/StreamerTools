# Audiobar Calculator
A simple script to calculate bar widths and spacing for audio bar visualizers.

## Features
- [x] Takes a given width in pixels
- [x] Optionally define a range for bar count, bar size and spacing

## Usage
`python audiobar_calc.py [-h] [-n-min N_MIN] [-n-max N_MAX] [-w-min W_MIN] [-w-max W_MAX] [-s-min S_MIN] [-s-max S_MAX] width`

Parameter    | Meaning
-------------|----------
-h, --help   | Shows a help message
-n-min N_MIN | Defines the minimum amount of bars
-n-max N_MAX | Defines the maximum amount of bars
-w-min W_MIN | Defines the minimum width of bars
-w-max W_MAX | Defines the maximum width of bars
-s-min S_MIN | Defines the minimum space between bars
-s-max S_MAX | Defines the maximum space between bars
width        | The size in pixels to fill with audiobars