# Backend Repository

1. Build **surrogate-model-backend.tar**
    1. Checkout the repository **bauers-ma** into any directory
    1. Place the files `mlp_best.joblib` and `mlp_classifier_best.joblip` (previously generated under `/model_training`) under `./backend/files/trained_model/`
    1. Build the image and save it to a *.tar*-file
    ```sh
    docker build -t surrogate-model-backend backend/
    docker save -o ./surrogate-model-backend.tar surrogate-model-backend
    ```
    1. Copy the file `surrogate-model-backend.tar ` into the direcotry `model_backend/`
3. Change into this directory (`model_backend/`)
4. Build **Litterbox Web** docker image and place **embedded-kittens.tar** into this directory or use the existing *.tar*-file
5. Start **embedded-kittens.sh**
6. Start **surrogate-model-backend.sh**
7. Now you can start with the whisker cluster experiments