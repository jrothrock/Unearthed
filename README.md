# Unearthed Denver 2017 Hackathon

This repository contains a solution for *Challenge 1: Man vs. Machine: Sort the Rocks* from the 
[Unearthed Denver 2017 Hackathon](https://unearthed.solutions/hackathons/unearthed-denver-2017/).

## How we labeled

To train the model, we created a few python scripts, `arw_to_tiff.py`, `data_prep_rename.py`, and `excelReader_rename.py`, which prepared the data set, and trained the model, by:
1. Splitting the 25 rock image files into individual rock images.
2. Labeling each photo based on what was assigned in the excel sheets.
3. Transfer learning using Google’s Inception V3 Neural Net.

## Real Time Predicting

To run real time predictions:
```
git clone git@github.com:jrothrock/Unearthed.git

cd ./unearthed/tensorflow

sudo -H pip install -r requirements.txt --ignore-installed

python real_time_classifier.py
```

## Docker - Training, and Predicting

To train the model, attach to the Docker instance
```
cd ./unearthed

docker run -it -v ./tensorflow:/tf_files/ gcr.io/tensorflow/tensorflow:latest-devel
```
Train model
```
cd /tf_files

python /tensorflow/tensorflow/examples/image_retraining/retrain.py \
  --bottleneck_dir=/tf_files/bottlenecks \
  --how_many_training_steps 4000 \
  --model_dir=/tf_files/inception \
  --output_graph=/tf_files/retrained_graph.pb \
  --output_labels=/tf_files/retrained_labels.txt \
  --image_dir /tf_files/data
```

Single Prediction
```
python single_classifier.py /tf_files/img/sets/img_to_predict_on.jpg
```

Multi Prediction When Images Are In Grids
```
python multi_grid_classifier.py /tf_files/img/sets/
```