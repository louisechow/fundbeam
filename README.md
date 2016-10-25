# FundBeam
Beam your payment to your friends!

FundBeam allows you to quickly send payments to your friends. Try it out!

## Prerequisites
FundBeam is a Django project. You will need to have the following installed on your computer before you start
- Python 3 (https://www.python.org/downloads/)
- Pip (https://pip.pypa.io/en/stable/installing/)
- VirtualEnv (http://docs.python-guide.org/en/latest/dev/virtualenvs/)

## Installation
- Get the FundBeam project from GitHub
```
git clone https://github.com/louisechow/fundbeam.git
```
- Create your virtual environment
```
virtualenv --python python3 env
source env/bin/activate
```
- Install the dependencies
```
cd <project_root>
pip install -r requirements.txt
```

## Running Tests
To run all the FundBeam tests, just execute the following command from the project root.
```
./manage.py test --pattern="test_*.py"

```
## Access the FundBeam application
To start the webapp, run the following command from the project root.
```
./manage.py runserver
```
Then just navigate to the local server at http://127.0.0.1:8000/ and you are ready to start using FundBeam.
