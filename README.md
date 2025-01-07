# AWS Agent

## Introduction
This is a python application developed with LLM through langchain and langgraph.


## Features
1. Fetch public s3 buckets and the data objects stored by a specific bucket.
2. Retrieves the size of the ec2 instance given an ip address
3. Retrieves the IAM permissions of a given user


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/duderrick/aws_agent.git
   ```

2. Install Python

   Ensure Python 3.11.9 or later is installed on your system.

3. Create a python virtual environment

   Replace <YOUR VIRTUAL ENV NAME> with your desired virtual environment name:
   ```
    python -m venv <YOUR VIRTUAL ENV NAME>
   ```
   
4. Activate the Virtual Environment

   If your virtual environment is installed at /home/users/user1/venvs/my_qt_env, activate it using:
   ```bash 
   source /home/users/user1/venvs/my_qt_env/bin/activate
   ```


#### Note
    
Before running the application, please modify the following lines in ***utils/constants.py***
        
        ```
        AWS_ACCESS_KEY_ID = '[AWS_ACCESS_KEY_ID]'
        AWS_SECRET_ACCESS_KEY = '[AWS_SECRET_ACCESS_KEY]'
        AWS_SESSION_TOKEN = ''
        ```

Please also enable the AWS Bedrock LLM models mentioned in ***utils/constants.py***


5. Install Dependencies

    a. Navigate to the cloned repository:
    ```bash
    cd <REPO_DIRECTORY>
    ```
   
    b. Install the required Python packages
    ```bash
    pip install -r requirements.txt
    ```

6. Run the application

    a. Configure your PYTHONPATH to include the root of the cloned source code.

   ```commandline
      on Windows: SET PYTHONPATH=[ABSOLUTE PATH]
      on Linux: export PYTHONPATH=[ABSOLUTE PATH]
   ```

    b. Run the application:
    ```bash
    python agents/aws_agent.py
    ```