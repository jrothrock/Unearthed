## Unearthed Denver 2017 Hackathon

This repository contains a solution for *Challenge 1: Man vs. Machine: Sort the Rocks* from the 
[Unearthed Denver 2017 Hackathon](https://unearthed.solutions/hackathons/unearthed-denver-2017/).

The python script, *utils/data_prep.py*, prepares the data set by
1. Splitting the 25 rock image files into individual rock images.
2. Labeling each photo based on what was assigned in the excel sheets.
3. Transfer learning using Google’s Inception V3 Neural Net.

To test a prediction, attach to the Docker instance
```
docker run -it -v $HOME/tf_files:/imgs/ gcr.io/tensorflow/tensorflow:latest-devel
```

Then run

```
python label_image.py /img/guess.jpg
```

To train model, test a prediction
```
python tensorflow/examples/image_retraining/retrain.py \
  --bottleneck_dir=/tf_files/bottlenecks \
  --how_many_training_steps 4000 \
  --model_dir=/tf_files/inception \
  --output_graph=/tf_files/retrained_graph.pb \
  --output_labels=/tf_files/retrained_labels.txt \
  --image_dir /tf_files/data
```