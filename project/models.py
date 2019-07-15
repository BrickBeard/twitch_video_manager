from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Table People ---------------------------------------------
class People(db.Model):
    __tablename__ = 'people'

    person_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=True)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    slack_username = db.Column(db.String(), nullable=True)
    twitch_username = db.Column(db.String(), nullable=True)
    twitter_handle = db.Column(db.String(), nullable=True)
    github_username = db.Column(db.String(), nullable=True)
    stream_trained_date = db.Column(db.Date, nullable=True)
    subscription_interest = db.Column(db.Boolean, nullable=True)
    code_of_conduct = db.Column(db.Boolean, nullable=True)
    # Table Relationships
    user_credentials = db.relationship('UserCredentials', backref='people', lazy=True)
    group_leaders = db.relationship('GroupLeaders', backref='people', lazy=True)
    group_mgmt_contact = db.relationship('Groups', backref='people', lazy=True)
    highlighters = db.relationship('Highlighters', backref='people', lazy=True)
    presentations = db.relationship('Presentations', backref='people', lazy=True)
    event_streamers = db.relationship('EventStreamers', backref='people', lazy=True)
    user_groups = db.relationship('UserGroups', backref='people', lazy=True)
    group_speakers = db.relationship('GroupSpeakers', backref='people', lazy=True)
    group_streamers = db.relationship('GroupStreamers', backref='people', lazy=True)

    def __init__(self, name, **kwargs):
        self.name = name
        super(People, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'person_id': self.person_id,
            'name': self.name, 
            'email': self.email,
            'admin': self.admin,
            'slack_username': self.slack_username,
            'twitch_username': self.twitch_username,
            'twitter_handle': self.twitter_handle,
            'github_username': self.github_username,
            'stream_trained_date': self.stream_trained_date,
            'subscription_interest': self.subscription_interest,
            'code_of_conduct': self.code_of_conduct
        }

    @property
    def is_admin(self):
        return self.admin
    
    def __repr__(self):
        return f'<Person {self.person_id}: {self.name}>'

# Table UserCredentials -----------------------------------
class UserCredentials(db.Model):
    __tablename__ = 'user_credentials'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('people.person_id'), nullable=False)
    hashed_password = db.Column(db.String(), nullable=True)
    password_salt = db.Column(db.String(), nullable=True)

    def __init__(self, user_id, hashed_password, password_salt):
        self.user_id = user_id
        self.hashed_password = hashed_password
        self.password_salt = password_salt

    def __repr__(self):
        return f'<UserCredentials {self.user_id}>'


# Table Groups ---------------------------------------------
class Groups(db.Model):
    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(), nullable=False)
    abbreviation = db.Column(db.String(), nullable=True)
    twitter_handle = db.Column(db.String(), nullable=True)
    meetup_url_name = db.Column(db.String(), nullable=True)
    meetup_weekday = db.Column(db.Integer, nullable=True)
    meetup_week = db.Column(db.Integer, nullable=True)
    meetup_time = db.Column(db.Time, nullable=True)
    mgmt_team_contact_id = db.Column(db.Integer, db.ForeignKey('people.person_id'), nullable=True)
    logo_link = db.Column(db.String(), nullable=True)
    # Table Relationships
    group_leaders = db.relationship('GroupLeaders', backref='groups', lazy=True)
    user_groups = db.relationship('UserGroups', backref='groups', lazy=True)
    group_speakers = db.relationship('GroupSpeakers', backref='groups', lazy=True)
    group_streamers = db.relationship('GroupStreamers', backref='groups', lazy=True)
    events = db.relationship('Events', backref='groups', lazy=True)

    def __init__(self, name, abbreviation, **kwargs):
        self.name = name
        super(Groups, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'group_id': self.group_id,
            'name': self.name,
            'abbreviation': self.abbreviation,
            'twitter_handle': self.twitter_handle,
            'meetup_url_name': self.meetup_url_name,
            'meetup_weekday': self.meetup_weekday,
            'meetup_week': self.meetup_week,
            'meetup_time': self.meetup_time,
            'mgmt_team_contact_id': self.mgmt_team_contact_id,
            'logo_link': self.logo_link
        }

    def __repr__(self):
        return f'<Group {self.name}>'

# Table GroupLeaders ---------------------------------------
class GroupLeaders(db.Model):
    __tablename__ = 'group_leaders'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.person_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)     

    def __init__(self, person_id, group_id):
        self.person_id = person_id
        self.group_id = group_id

    @property
    def serialize(self):
        return {'person_id': self.person_id, 'group_id': self.group_id}

    def __repr__(self):
        return f'<GroupLeader {self.person_id}, {self.group_id}>'

# Table Highlighters ---------------------------------------
class Highlighters(db.Model):
    __tablename__ = 'highlighters'

    id = db.Column(db.Integer, primary_key=True)
    highlighter_id = db.Column(db.Integer, db.ForeignKey('people.person_id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'), nullable=False)     

    def __init__(self, highlighter_id, video_id):
        self.highlighter_id = highlighter_id
        self.video_id = video_id

    @property
    def serialize(self):
        return {'highlighter_id': self.highlighter_id, 'video_id': self.video_id}

    def __repr__(self):
        return f'<Highlighter {self.highlighter_id}, {self.video_id}>'

# Table Presentations ---------------------------------
class Presentations(db.Model):
    __tablename__ = 'presentations'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.person_id'), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=True)     
    title = db.Column(db.String(), nullable=True)
    summary = db.Column(db.String(), nullable=True)
    bio = db.Column(db.String(), nullable=True)
    stream_consent = db.Column(db.Boolean, nullable=True)
    keyword_list = db.Column(db.String(), nullable=True)
    links = db.Column(db.String(), nullable=True)
    audio_in_presentation = db.Column(db.Boolean, nullable=True)
    hdmi_adapter = db.Column(db.String(), nullable=True)
    talk_length_minutes = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String(), nullable=True)

    def __init__(self, **title):
        super(Presentations, self).__init__(**title)

    @property
    def serialize(self):
        return {
            'person_id': self.person_id, 
            'event_id': self.event_id, 
            'title': self.title,
            'summary': self.summary,
            'bio': self.bio,
            'stream_consent': self.stream_consent,
            'keyword_list': self.keyword_list,
            'links': self.links,
            'audio_in_presentation': self.audio_in_presentation,
            'hdmi_adapter': self.hdmi_adapter,
            'talk_length_minutes': self.talk_length_minutes,
            'notes': self.notess
        }

    def __repr__(self):
        return f'<Presentation {self.event_id}>'

# Table EventStreamers -------------------------------------
class EventStreamers(db.Model):
    __tablename__ = 'event_streamers'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.person_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)     

    def __init__(self, person_id, event_id):
        self.person_id = person_id
        self.event_id = event_id

    @property
    def serialize(self):
        return {'person_id': self.person_id, 'event_id': self.event_id}

    def __repr__(self):
        return f'<EventStreamer {self.person_id}, {self.event_id}>'

# Table UserGroups -----------------------------------------
class UserGroups(db.Model):
    __tablename__ = 'user_groups'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.person_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)     

    def __init__(self, person_id, group_id):
        self.person_id = person_id
        self.group_id = group_id

    @property
    def serialize(self):
        return {'person_id': self.person_id, 'group_id': self.group_id}

    def __repr__(self):
        return f'<UserGroup {self.person_id}, {self.group_id}>'

# Table GroupSpeakers --------------------------------------
class GroupSpeakers(db.Model):
    __tablename__ = 'group_speakers'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.person_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)     

    def __init__(self, person_id, group_id):
        self.person_id = person_id
        self.group_id = group_id

    @property
    def serialize(self):
        return {'person_id': self.person_id, 'group_id': self.group_id}

    def __repr__(self):
        return f'<GroupSpeaker {self.person_id}, {self.group_id}>'

# Table GroupStreamers -------------------------------------
class GroupStreamers(db.Model):
    __tablename__ = 'group_streamers'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.person_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)  
    default = db.Column(db.Boolean, default=False)   

    def __init__(self, person_id, group_id, **default):
        self.person_id = person_id
        self.group_id = group_id
        super(GroupStreamers, self).__init__(**default)

    @property
    def serialize(self):
        return {'person_id': self.person_id, 'group_id': self.group_id, 'default': self.default}

    def __repr__(self):
        return f'<GroupStreamer {self.person_id}, {self.group_id}>'

# Table Locations ------------------------------------------
class Locations(db.Model):
    __tablename__ = 'locations'

    location_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=True) 
    city = db.Column(db.String(), nullable=True)
    state = db.Column(db.String(), nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)
    website = db.Column(db.String(), nullable=True)
    twitter_handle = db.Column(db.String(), nullable=True)
    # Table Relationships
    events = db.relationship('Events', backref='locations', lazy=True)

    def __init__(self, name, city, state, **kwargs):
        self.name = name
        super(Locations, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'location_id': self.location_id,
            'name': self.name, 
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'website': self.website,
            'twitter_handle': self.twitter_handle
        }

    def __repr__(self):
        return f'<Location {self.location_id}, {self.name}>'

# Table LocationContacts -------------------------------------
class LocationContacts(db.Model):
    __tablename__ = 'location_contacts'

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.person_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)     

    def __init__(self, person_id, location_id):
        self.person_id = person_id
        self.location_id = location_id

    @property
    def serialize(self):
        return {'person_id': self.person_id, 'location_id': self.location_id}

    def __repr__(self):
        return f'<LocationContact {self.person_id}, {self.location_id}>'

# Table Videos ---------------------------------------------
class Videos(db.Model):
    __tablename__ = 'videos'

    video_id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'), nullable=True)
    twitch_id = db.Column(db.Integer, nullable=True)
    youtube_id = db.Column(db.Integer, nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=True) 
    title = db.Column(db.String(), nullable=True)
    description = db.Column(db.String(), nullable=True)
    # Table Relationships
    highlighters = db.relationship('Highlighters', backref='videos', lazy=True)

    def __init__(self, **kwargs):
        super(Videos, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'video_id': self.video_id, 
            'parent_id': self.parent_id, 
            'twitch_id': self.twitch_id,
            'youtube_id': self.youtube_id, 
            'event_id': self.event_id, 
            'title': self.title,
            'description': self.description
        }

    def __repr__(self):
        return f'<Video {self.video_id}, {self.title}>'

# Table Events ---------------------------------------------
class Events(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True) 
    group_id = db.Column(db.Integer, nullable=True)
    meetup_id = db.Column(db.String(), nullable=True)
    title = db.Column(db.String(), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    speaker_form = db.Column(db.Boolean, nullable=True)
    venue_booked = db.Column(db.Boolean, nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=True)
    # Table Relationships
    presentations = db.relationship('Presentations', backref='events', lazy=True)
    event_streamers = db.relationship('EventStreamers', backref='events', lazy=True)
    videos = db.relationship('Videos', backref='events', lazy=True)

    def __init__(self, title, **kwargs):
        self.title = title
        super(Events, self).__init__(**kwargs)

    @property
    def serialize(self):
        return {
            'event_id': self.event_id,
            'group_id': self.group_id,
            'meetup_id': self.meetup_id,
            'title': self.title,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'stream': self.stream,
            'speaker_form': self.speaker_form,
            'venue_booked': self.venue_booked,
            'location_id': self.location_id
        }

    def __repr__(self):
        return f'<Event {self.event_id}>'