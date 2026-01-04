# Replication package

## General
TODO: Bla bla bla...

## Steps

1. Setup the environment in `environment/`
1. Checkout variants into `variants/`
1. Process these in `variants_out/` in order to get the training data for the models
1. Train the models whith the generated training data in `model_training/`
1. Place models in `bauers-ma/backend/files/trained_model/`
1. Start the surrogate model backend in `bauers-ma/surrogate-model/`
1. Prepare and start whisker-cluster-experiments
    1. Checkout whisker with branch *automatic-repair-surrogate-model*
    1. Create configs

TODO: Describe folders with their orders


> df in model_training wird erzeugt -> Testen des trainings
