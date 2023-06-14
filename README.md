
# Iskowela: Student Recruitment Platform and Marketing Tool for Educational Institutions

Github repository link: https://github.com/jltsang/Iskowela-Final

## Authors
- [@jltsang](https://www.github.com/jltsang)
- [@likaelvan](https://www.github.com/likaelvan)

## Run Project
1. Install [Docker](https://www.docker.com/) and start the Docker Engine by opening the app.

2. Clone the repository at https://github.com/jltsang/Iskowela-Final.

  	```bash
      git clone https://github.com/jltsang/Iskowela-Final
  	```

3. Open terminal and go to the project directory.
4. To build and deploy the project through Docker, simply enter the command.

    ```bash
      docker compose up --build
    ```

* Main application is accessible through http://localhost:8000/
* The admin page can be accessed by going to http://localhost:8000/admin
## Run Independent Modules

If you currently do not have Docker installed and would wish to run the modules independently from one another, follow the steps below.

1. Clone the repository at https://github.com/jltsang/Iskowela-Final.

    ```bash
      git clone https://github.com/jltsang/Iskowela-Final
    ```

2. Open the following files

    ```bash
      Iskowela-Final\Iskowela\chatbot\views.py
      Iskowela-Final\rasa_chatbot\actions\actions.py
      Iskowela-Final\rasa_chatbot\endpoints.yml
    ```

3. Search for the respective urls and modify accordingly

    ```bash
      http://rasa:5005/webhooks/rest/webhook -> http://localhost:5005/webhooks/rest/webhook
      http://django:8000/ -> http://localhost:8000/
      http://action_server:5055/webhook -> http://localhost:5055/webhook
    ```

4. Install required dependencies

    * Change directory to **Iskowela-Final\Iskowela** and run the followning command

        ```bash
        pip install -r requirements.txt
        ```

    * Install rasa

        ```bash
        pip install rasa
        ```

    * **Note**: If there are issues with Rasa installation, try to downgrade your Python version to 3.9+
    
5. Once all dependencies have been installed, the wesbite can be run locally by starting the Django server

    * Change directory to **Iskowela-Final\Iskowela**

    * Start the Django server using the command

        ```bash
        python manage.py runserver
        ```

6. Rasa can be run locally by running rasa open source and rasa action server

    * Change directory to **Iskowela-Final\rasa_chatbot**

    * Start the rasa server with the trained model using the command

        ```bash
        rasa run 
        ```

    * Change directory to **Iskowela-Final\rasa_chatbot\actions**

    * Start the action server using the command
        ```bash
        rasa run actions
        ```
        
## Other Notes

* All three must be running for the whole project to work properly. The chatbot module will not work if Rasa is not running.

* To talk directly to the assistant from the command line, run
     ```bash
    rasa shell
    ```
        
* To train new rasa models, run
     ```bash
    rasa train
    ```
