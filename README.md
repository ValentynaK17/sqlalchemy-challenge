# sqlalchemy-challenge
Basic climate analysis and data exploration of a climate database, using SQLAlchemy ORM queries, Pandas, and Matplotlib with Flask API, based on the queries, which outputs data in JSON format
## Repository Contents
  - **SQLAlchemy_Flask** directory contains:
    - *climate_analysis.ipynb*, which focuses on analysis of data for 1 year time duration<br>
    - *app.py*, which outputs the above analysis into Flask API endpoints in JSON format  <br>
  - **Resources** directory contains hawaii.sqlite, used as an input data. It also contains 2 csv files for reference, which were not used in scripts though <br>
## Resources
 - [How to recognize null value in python](https://www.copahost.com/blog/null-python/#:~:text=In%20Python%2C%20the%20null%20value,a%20variable%20is%20not%20initialized)
 - ["and" operation in SQLAlchemy](https://www.youtube.com/watch?v=woKYyhLCcnU)
 - [convert string into date object: part1](https://www.datacamp.com/tutorial/converting-strings-datetime-objects?utm_source=google&utm_medium=paid_search&utm_campaignid=19589720821&utm_adgroupid=157156375191&utm_device=c&utm_keyword=&utm_matchtype=&utm_network=g&utm_adpostion=&utm_creative=676354849169&utm_targetid=dsa-2218886984100&utm_loc_interest_ms=&utm_loc_physical_ms=9000976&utm_content=&utm_campaign=230119_1-sea~dsa~tofu_2-b2c_3-row-p1_4-prc_5-na_6-na_7-le_8-pdsh-go_9-na_10-na_11-na-oct23&gad_source=1&gclid=CjwKCAjwv-2pBhB-EiwAtsQZFJ5LwlAwSNCOPqfBTj2rX8IKReUztuY-45YFOXgwcjvtJh4dI9RA8BoCchUQAvD_BwE)
 - [convert string into date object: part2](https://www.programiz.com/python-programming/datetime)
## Installation
Having Python installed on your machine along with Jupyter Notebook available, clone this repository to your local machine
## Usage
 - Navigate to the **SQLAlchemy_Flask** directory
 - Run the *climate_analysis.ipynb* script using Jupyter Notebook
 - Run the *app.py* using Python (e.g. "python app.py") having the directory with a file as current; The address to access the application, will be shown in the terminal output
 - Access the API endpoints via web browser

