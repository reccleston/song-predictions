create table top_songs (
    song varchar,
    performer varchar,
    chart_position float,
    previous_position float,
    peak float,
    weeks_on_chart float,
    hitTF float,
    id varchar,
    danceability float,
    energy float,
    key float,
    loudness float,
    mode float,
    speechiness float,
    acousticness float,
    instrumentalness float,
    liveness float,
    valence float,
    tempo float,
    duratin_ms float,
    time_signature float
);

create table dates (
    chart_week date
);

ALTER TABLE dates ADD PRIMARY KEY (chart_week);

create table latest_data (
    song varchar,
    performer varchar,
    chart_position float,
    previous_position float,
    peak float,
    weeks_on_chart float,
    hitTF float,
    id varchar,
    danceability float,
    energy float,
    key float,
    loudness float,
    mode float,
    speechiness float,
    acousticness float,
    instrumentalness float,
    liveness float,
    valence float,
    tempo float,
    duratin_ms float,
    time_signature float
);

ALTER TABLE latest_data ADD PRIMARY KEY (id);