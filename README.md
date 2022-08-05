This project fetches vessel info between the given longitude and latitiude from MarineTraffic. The (MinLat,MaxLat) and (MinLongi, MaxLongi) should be given as terminal argument. An example can be seen below.

# First time opening the project

## Install python 3.10
### Using windows
* Open Microsoft Store.
* Type Python 3.10 on search bar.
* Select Python 3.10 and install it.
### Using unix
Follow below steps
```
sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10
```

## Install python virtualenv lib
pip install virtualenv
## Create a virtual environment
python -m venv env
## Activate the virtual environment
### Using unix
source env/bin/activate 
### Using windows 
env\Scripts\activate 
## To install dependecies of the project: 
pip install -r requirements.txt
## Example scrape and send to localhost:5005:
python main.py --p 1 --lat-min 40.83 --lat-max 40.875 --lon-min 29.233 --lon-max 29.292
## To test the data transmiting over UDP while the main script is running:
python test_receive.py

# Second time opening the project

## Activate the virtual environment
### Using unix
source env/bin/activate 
### Using windows 
env\Scripts\activate 
## Example scrape and send to localhost:5005:
python main.py --p 1 --lat-min 40.83 --lat-max 40.875 --lon-min 29.233 --lon-max 29.292
## Example scrape and print to console:
python main.py --p 0 --lat-min 40.83 --lat-max 40.875 --lon-min 29.233 --lon-max 29.292
## To test the data transmiting over UDP while the main script is running:
python test_receive.py
