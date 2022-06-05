# Explanation of Code

### Model Selection and basic parameter setup
Out of the two baseline models given to us, the CNN model was computationally expensive to run, as compared to XGBoost which enabled faster experimentation, and provided very equivalent performance.
While the efficiency of Boosting algorithms made it the obvious choice, we tried a few other models like LightGBM but witnessed very similar performance, hence proceeded with XGBoost
We decided to build two separate models specific to Urban and Rural labels.
We have also decided to play around with a tree depth of 2/3, and the shrinkage parameter we have set it up to be 0.18 to avoid overfitting in general.

### Feature Encoding
We used KDTrees Encoding as a preprocessing step as given in the baseline with a few upgrades

We used 500 images but we are limited to these many images because of memory issues however we shall try it locally to use more images for extracting features
We also tried Ball Trees instead of KDTrees but no significant improvement was noticed, hence we proceeded with KDTrees with the above implemented upgrades.

### Data Augmentation
We are planning to increase our training data by augmentating images so we will have approximately 5 variations of one image (rotate, flip, etc). Due to memory issues, currently we have been able to generate 3000 images. This change shall be implemented in the next iteration/submission.

### Creating metrics to quantify performance
We have added custom metrics such as F1 score to check performance on our training set inside the XGBoost algorithm. 
We have also included more parameters to tune in our XGBoost model such as feature_selector, verbose_eval, early_stopping_rounds, etc. We have also added code for grid search CV to find optimal parameters (not implemented in this version).


### Using better split ratios between train and validation sets
We tried different combinations to test which ratio works the best, currently we have decided to proceed with 70-30% split between train and validation dataset for both rural and urban specific models, but we shall increase our training size (using either a different split ratio or adding the augmented images) in future iterations/submissions so that the model can learn better.


### Setting custom thresholds 
In this submission we have decided to go ahead with 1.25*std>mean for both models to avoid negative scores, but in future submissions to improve test set performance we might tune the thresholds according to our convenience.