## Unearthed Denver 2017 Hackathon

This repository contains a solution for *Challenge 1: Man vs. Machine: Sort the Rocks* from the 
[Unearthed Denver 2017 Hackathon](https://unearthed.solutions/hackathons/unearthed-denver-2017/).

The python script, *utils/data_prep.py*, prepares the data set by converting the image files to a pickle file with two *numpy arrays*:
```
data: Array of shape (N, W, H, C), where
  N is the number of rocks
  W is the width of each rock
  H is the height of each rock
  C is the number of color channels, 3 for RGB

labels: Array of shape (N, 1)
```
