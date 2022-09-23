# KU-Poll

## Online Polls for Kasetsart University

An application for conducting a poll or survey, written in Python using Django. It is based on the [Django Tutorial project][django-tutorial],
with additional functionality.

This application is part of the [Individual Software Process](https://cpske.github.io/ISP) course at [Kasetsart University](https://ku.ac.th).

## How to Install and Run
1. Clone this project repository.
    ```
    git clone https://github.com/natekrth/ku-polls.git
    ```
2. Go in to ku-polls directory.
    ```
    cd ku-polls
    ```
3. Create a virtual environment.
    ```
    python3 -m venv env
    ```
4. Start the virtual environment.  

    on macos and linux
    ```
    source env/bin/activate 
    ```
    on windows
    ```
    . env/bin/activate
    ```
5. Install required packages.
    ```
    pip install -r requirements.txt
    ```
6. Create `.env` and write.
    ```
    SECRET_KEY = secret-key-value-without-quotes 
    DEBUG = False
    TIME_ZONE = Asia/Bangkok
    ALLOWED_HOSTS = localhost,127.0.0.1
    ```
7. Create a new database by running migrations the database.
    ```
    python3 manage.py migrate
    ```
8. Import and Export the database.  

    8.1 Import the database (Do This!).  
    ```
    python3 manage.py loaddata
    ```
    You can try
    ```
    python3 manage.py loaddata data/polls.json data/users.json
    ```
    
    8.2 Export the database (Optional). 
    ```
    python3 manage.py dumpdata
    ```
    Try dump all polls data to a file (`-o`) named polls.json
    ```
    python3 manage.py dumpdata --indent=2 -o polls.json polls
    ```
9. Start running server.
    ```
    python3 manage.py runserver
    ```

### Demo User

| Username  | Password  |
|-----------|-----------|
|   tester  | nohack1234|
|   hacker  | hackme22  |

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home)

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Development%20Plan)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan) | [Iteration 1 Task Board](https://github.com/users/natekrth/projects/1/views/1) 
- [Iteration 2 Plan](../../wiki/Iteration-2-Plan) | [Iteration 2 Task Board](https://github.com/users/natekrth/projects/1/views/3)
- [Iteration 3 Plan](../../wiki/Iteration-3-Plan) | [Iteration 3 Task Board](https://github.com/users/natekrth/projects/1/views/4)
- [Iteration 4 Plan](../../wiki/Iteration-4-Plan) | [Iteration 4 Task Board](https://github.com/users/natekrth/projects/1/views/5)