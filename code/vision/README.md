# Vision Module

This folder contains the **pose and depth estimation** notebook used in the paper for deployment-oriented perception and digital-twin alignment.

## Included file

- `Pose_and_Depth.ipynb`  
  A step-by-step notebook for microscope-image-based pose prediction and depth estimation.

## What the notebook covers

The notebook includes the main stages of the perception pipeline:

- loading labelled microscope images
- parsing pose / depth labels
- dataset splitting for training / validation / testing
- multitask learning for pose-related prediction and depth regression
- model training
- quantitative evaluation and result visualisation

## How to use

1. Open `Pose_and_Depth.ipynb` in Jupyter Notebook or VS Code.
2. Update the local dataset paths and output paths in the notebook.
3. Run the cells in order from data loading to training and evaluation.
4. Save the trained weights and predicted results for later digital-twin reconstruction if needed.

## Suggested future contents

If needed, this folder can also include:

- `checkpoints/`
- `configs/`
- `samples/`
- exported prediction results
