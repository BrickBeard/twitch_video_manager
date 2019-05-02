# Techlahoma Twitch Video Manager

[![built-with-Flask](https://img.shields.io/badge/Built%20With-Flask%201.0.2-brightgreen.svg?style=flat-square)](http://flask.pocoo.org/) [![Python-Version](https://img.shields.io/badge/Python-3.7-orange.svg?style=flat-square)](https://www.python.org/downloads/) [![Testing](https://img.shields.io/badge/Testing-Pytest-blue.svg?style=flat-square)](https://docs.pytest.org/en/latest/)


This app is currently designed to identify which terchlahoma broadcasts are still in need of highlights (the broadcasts expire after 60 days if they have not been highlighted).  The future vision for the app includes automating most steps of the broadcasting, highlighting, and exporting process.  

---

## Instructions

First clone the repo and initialize a virtualenv:
```
$ git clone https://github.com/BrickBeard/twitch_video_manager.git
$ cd twitch_video_manager
$ virtualenv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
```
Next, create a `.env` file and add in the following information:
```
FLASK_ENV=development
CLIENT_ID='your_twitch_client_id_here'
```
> To get a `Twitch Client ID` you need to: 
> - Create a developer account with Twitch **[Here](https://dev.twitch.tv)**
> - Register your application **[Here](https://dev.twitch.tv/console/apps/create)** (or simply navigate to `Dashboard` > `Applications` > [![Register](https://img.shields.io/badge/Register_Your_Application-blue.svg?style=round-square)](#)):
>   - `name` (up to you)
>   - `URL` (**http://localhost**)
> - Copy your `Client ID` and add it to the `.env` file

### Run App!

```
flask run
```

---

## Testing The App:

Simply type:  
```
$ pytest
```

  

### Questions or Comments

Please leave feedback on here or reach out to me on the Techlahoma Slack **@brickbeard**
