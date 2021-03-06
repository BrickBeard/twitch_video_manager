"""empty message

Revision ID: c5738a6ca907
Revises: 
Create Date: 2019-06-19 13:27:49.705962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5738a6ca907'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('zipcode', sa.Integer(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('twitter_handle', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('location_id')
    )
    op.create_table('people',
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.Column('slack_username', sa.String(), nullable=True),
    sa.Column('twitch_username', sa.String(), nullable=True),
    sa.Column('twitter_handle', sa.String(), nullable=True),
    sa.Column('github_username', sa.String(), nullable=True),
    sa.Column('stream_trained_date', sa.Date(), nullable=True),
    sa.Column('subscription_interest', sa.Boolean(), nullable=True),
    sa.Column('code_of_conduct', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('person_id')
    )
    op.create_table('events',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('meetup_id', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('speaker_form', sa.Boolean(), nullable=True),
    sa.Column('venue_booked', sa.Boolean(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.location_id'], ),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_table('groups',
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('abbreviation', sa.String(), nullable=True),
    sa.Column('twitter_handle', sa.String(), nullable=True),
    sa.Column('meetup_url_name', sa.String(), nullable=True),
    sa.Column('meetup_weekday', sa.Integer(), nullable=True),
    sa.Column('meetup_week', sa.Integer(), nullable=True),
    sa.Column('meetup_time', sa.Time(), nullable=True),
    sa.Column('mgmt_team_contact_id', sa.Integer(), nullable=True),
    sa.Column('logo_link', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['mgmt_team_contact_id'], ['people.person_id'], ),
    sa.PrimaryKeyConstraint('group_id')
    )
    op.create_table('location_contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['locations.location_id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['people.person_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_credentials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('password_salt', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['people.person_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_streamers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.event_id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['people.person_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group_leaders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.group_id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['people.person_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group_speakers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.group_id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['people.person_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group_streamers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.group_id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['people.person_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('presentations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('summary', sa.String(), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('stream_consent', sa.Boolean(), nullable=True),
    sa.Column('keyword_list', sa.String(), nullable=True),
    sa.Column('links', sa.String(), nullable=True),
    sa.Column('audio_in_presentation', sa.Boolean(), nullable=True),
    sa.Column('hdmi_adapter', sa.String(), nullable=True),
    sa.Column('talk_length_minutes', sa.Integer(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.event_id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['people.person_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.group_id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['people.person_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('videos',
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('twitch_id', sa.Integer(), nullable=True),
    sa.Column('youtube_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.event_id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['videos.video_id'], ),
    sa.PrimaryKeyConstraint('video_id')
    )
    op.create_table('highlighters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('highlighter_id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['highlighter_id'], ['people.person_id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['videos.video_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('highlighters')
    op.drop_table('videos')
    op.drop_table('user_groups')
    op.drop_table('presentations')
    op.drop_table('group_streamers')
    op.drop_table('group_speakers')
    op.drop_table('group_leaders')
    op.drop_table('event_streamers')
    op.drop_table('user_credentials')
    op.drop_table('location_contacts')
    op.drop_table('groups')
    op.drop_table('events')
    op.drop_table('people')
    op.drop_table('locations')
    # ### end Alembic commands ###
