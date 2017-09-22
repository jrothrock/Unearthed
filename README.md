## Unearthed Denver 2017 Hackathon

This repository contains a solution for *Challenge 1: Man vs. Machine: Sort the Rocks* from the 
[Unearthed Denver 2017 Hackathon](https://unearthed.solutions/hackathons/unearthed-denver-2017/).

The python script, *utils/data_prep.py*, prepares the data set by
1. Splitting the 25 rock image files into individual rock images
2. Resizing each image from a (width, height) of (772, 463) to (224, 136)
3. Creating a data array for the rocks and a label array for the assigned rock type, then writing these to the file data.pickle.

```
data: Array of shape (N, H, W, C), where
  N is the number of rocks
  H is the height of each rock
  W is the width of each rock
  C is the number of color channels, 3 for RGB

labels: Array of shape (N, 1)
```
