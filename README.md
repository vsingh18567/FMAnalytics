# FM Analytics

FM Analytics is a web-app in progress that allows users to upload game data from the Football Manager series, and have it stored, processed and analysed. It will rely on using a particular Steam Workshop item to standardise the format of the game data. The `sampleData` folder has examples of the game data that gets processed. 

## View the Website
`$ls` should show the `manage.py` file. 
```
$ pip install -r requirements.txt
$ python manage.py runserver
```
To trial with a dummy user that has the dummy data loaded
```
username: dummyuser
password: dummypassword
```

## Apps
- `homePage` handles the home view and the various authentication processes
- `mainApp` handles the CRUD operations and data analysis 