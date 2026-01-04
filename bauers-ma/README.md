# Backend Repository

1. Checkout the bauers-ma repository in this folder
2. Place the files `mlp_best.joblib` and `mlp_classifier_best.joblip` (previously generated under `/model_training`) under `./backend/files/trained_model/`
3. Change into directory `./surrogate-model-backend/`
4. Build **Litterbox Web** docker image and place **embedded-kittens.tar** into this directory
5. Start **embedded-kittens.sh**
6. Start **surrogate-model-backend.sh**
7. TODO: Now you can start whisker cluster experiments