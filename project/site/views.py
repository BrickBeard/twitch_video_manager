import requests
import datetime
import json
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
        resp = requests.get('https://api.twitch.tv/helix/videos', headers=data, params=payload)
        response = json.loads(resp.text)
        videos.extend(response['data'])
        payload.pop('after')
        if not response['pagination'] == {}:
            payload.update({'after': response['pagination']['cursor']})
        else:
            payload['after'] = False
    return render_template('index.html', data={'videos': videos})

@site.route('/highlights')
def videos_highlight():
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

    from collections import Counter
    titles = Counter([v['title'].strip().replace('Highlight: ', '')[:20] for v in videos])
    counter = [k for k, v in titles.items() if v==1]
    videos_ = [v for v in videos if v['title'].strip().replace('Highlight: ', '')[:20] in counter and v['type'] == 'archive' and 'promos' not in v['title'].lower()]

    from io import BytesIO
    import base64
    for v in videos_:
        contents = BytesIO(requests.get(v["thumbnail_url"].replace("%","").format(width=200,height=110)).content)
        encoded = str(base64.b64encode(contents.getvalue()))[2:-1]
        v['thumbnail_url'] = encoded
        v['days'] = (datetime.datetime.today() - datetime.datetime.fromisoformat(v['created_at'][:-1])).days

    return render_template('highlights.html', data={'videos': videos_})


# MEETUP API INTEGRATION: Currently not automated but would be great to figure out
'''
@site.route('/video')
def video():
    id_ = request.args.get('id')
    twitch_params = {'id': id_}
    data = {'Client-ID': client_id}
    response = json.loads(requests.get('https://api.twitch.tv/helix/videos', headers=data, params=twitch_params).text)
    video = response['data']

    meetup = [{'something': 'coming'}]
    created_date = datetime.datetime.fromisoformat(video[0]['created_at'][:-1])
    start_date = created_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = created_date.replace(hour=23, minute=59, second=59, microsecond=0)
    print(f'created_date: {start_date.strftime("%Y-%m-%dT%H:%M:%S.000")}\nend_date: {end_date.strftime("%Y-%m-%dT%H:%M:%S.000")}')
    meetup_params = {"no_earlier_than": start_date.strftime("%Y-%m-%dT%H:%M:%S.000"), "no_later_than": end_date.strftime("%Y-%m-%dT%H:%M:%S.000"), 'status': 'past'}
    response = json.loads(requests.get('https://api.meetup.com/DevopsOKC/events', params=meetup_params).text)
    print(f'response: {response}')
    meetup = response[0]
    
    return render_template('video.html', data = {'video': video, 'meetup': meetup})
'''