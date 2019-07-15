import requests
import datetime
import json
import base64
from collections import Counter
from io import BytesIO
from flask import render_template, request, redirect, Blueprint, jsonify
from project.config import client_id, user_id


# Blueprint Declaration
site = Blueprint(
    'site',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# Views
@site.route('/')
def index():
    payload = {'user_id': user_id, 'first': 100}
    data = {'Client-ID': client_id}
    response = json.loads(requests.get('https://api.twitch.tv/helix/videos', headers=data, params=payload).text)
    videos = response['data']
    payload.update({'after': response['pagination']['cursor']})
    while payload['after']:
        try: 
            resp = requests.get('https://api.twitch.tv/helix/videos', headers=data, params=payload)
            response = json.loads(resp.text)
            videos.extend(response['data'])
            payload.pop('after')
            if not response['pagination'] == {}:  
                payload.update({'after': response['pagination']['cursor']})
            else:
                payload['after'] = False
        except KeyError:
            return "<br><br><h1 style='text-align: center;'>Error loading content...</h1><p style='text-align: center;'>Please try to <a href='/'>refresh</a> the page</p>"    
    for v in videos:
        v['created_at'] = datetime.datetime.fromisoformat(v['created_at'][:-1]).strftime("%b %d, %Y")
        if ':' in v['title']:
            v['group'] = v['title'][v['title'].rfind(':')+2:]
        else:
            v['group'] = '#Techlahoma'

    return render_template('index.html', data={'videos': videos})

@site.route('/pending')
def pending():
    payload = {'user_id': user_id, 'first': 100}
    data = {'Client-ID': client_id}
    response = json.loads(requests.get('https://api.twitch.tv/helix/videos', headers=data, params=payload).text)
    videos = response['data']
    payload.update({'after': response['pagination']['cursor']})
    while payload['after']:
        try: 
            resp = requests.get('https://api.twitch.tv/helix/videos', headers=data, params=payload)
            response = json.loads(resp.text)
            videos.extend(response['data'])
            payload.pop('after')
            if not response['pagination'] == {}:  
                payload.update({'after': response['pagination']['cursor']})
            else:
                payload['after'] = False
        except Exception as e:
            return "<br><br><h1 style='text-align: center;'>Error loading content...</h1><p style='text-align: center;'>Please try to <a href='/pending'>refresh</a> the page</p>"

    for v in videos:
        v['days'] = (datetime.datetime.today() - datetime.datetime.fromisoformat(v['created_at'][:-1])).days
        if ':' in v['title']:
            v['group'] = v['title'][v['title'].rfind(':')+2:]
        else:
            v['group'] = '#Techlahoma'

    titles = Counter([v['title'].strip().replace('Highlight: ', '')[:20] for v in videos])
    counter_title = [k for k, v in titles.items() if v==1]
    videos_ = [v for v in videos if v['title'].strip().replace('Highlight: ', '')[:20] in counter_title and v['type'] == 'archive' and 'promos' not in v['title'].lower() and 'lightning talk' not in v['title'].lower()]
    lightning_ = [v for v in videos if v['title'].strip().replace('Highlight: ', '')[:20] in counter_title and 'Lightning Talk' in v['title'] and v['days'] < 60 and v['type'] == 'archive']

    for v in videos_:
        contents = BytesIO(requests.get(v["thumbnail_url"].replace("%","").format(width=200,height=110)).content)
        encoded = str(base64.b64encode(contents.getvalue()))[2:-1]
        v['thumbnail_url'] = encoded

    # This loop is used to convert and format the thumbnail_url so we can display it on the site
    for l in lightning_:
        contents_ = BytesIO(requests.get(l["thumbnail_url"].replace("%","").format(width=200,height=110)).content)
        encoded_ = str(base64.b64encode(contents_.getvalue()))[2:-1]
        l['thumbnail_url'] = encoded_        

    return render_template('pending.html', data={'videos': videos_, 'lightning': lightning_})

@site.route('/highlights')
def highlights():
    payload = {'user_id': user_id, 'first': 100}
    data = {'Client-ID': client_id}
    response = json.loads(requests.get('https://api.twitch.tv/helix/videos', headers=data, params=payload).text)
    videos = response['data']
    payload.update({'after': response['pagination']['cursor']})
    while payload['after']:
        resp = requests.get('https://api.twitch.tv/helix/videos', headers=data, params=payload)
        response = json.loads(resp.text)
        videos.extend(response['data'])
        payload.pop('after')
        if not response['pagination'] == {}:
            payload.update({'after': response['pagination']['cursor']})
        else:
            payload['after'] = False
    
    videos_ = [v for v in videos if v['type'] == 'highlight']
    
    for v in videos_:
        v['created_at'] = datetime.datetime.fromisoformat(v['created_at'][:-1]).strftime("%b %d, %Y")
        if ':' in v['title']:
            v['group'] = v['title'][v['title'].rfind(':')+2:]
        else:
            v['group'] = '#Techlahoma'

    return render_template('highlights.html', data={'videos': videos_})

# Reference Route 
@site.route('/video')
def video():
    id_ = request.args.get('id')
    twitch_params = {'id': id_}
    data = {'Client-ID': client_id}
    response = json.loads(requests.get('https://api.twitch.tv/helix/videos', headers=data, params=twitch_params).text)
    video = response['data']
    ''' Meetup API Integration:
        (Ideally, this would call the Meetup API and grab information about this talk using some
        identifying field from the Twitch API call above.)

    meetup = [{'something': 'coming'}]
    created_date = datetime.datetime.fromisoformat(video[0]['created_at'][:-1])
    start_date = created_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = created_date.replace(hour=23, minute=59, second=59, microsecond=0)
    print(f'created_date: {start_date.strftime("%Y-%m-%dT%H:%M:%S.000")}\nend_date: {end_date.strftime("%Y-%m-%dT%H:%M:%S.000")}')
    meetup_params = {"no_earlier_than": start_date.strftime("%Y-%m-%dT%H:%M:%S.000"), "no_later_than": end_date.strftime("%Y-%m-%dT%H:%M:%S.000"), 'status': 'past'}
    response = json.loads(requests.get('https://api.meetup.com/DevopsOKC/events', params=meetup_params).text)
    print(f'response: {response}')
    meetup = response[0]
    '''
    return render_template('video.html', data = {'video': video})

# Test Route
# @site.route('/test')
# def test():
