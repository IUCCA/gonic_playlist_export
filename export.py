from sqlalchemy import *
import datetime

engine = create_engine('sqlite:///gonic.db')
conn = engine.connect()
metadata = MetaData()
albums = Table("albums", metadata,
               Column("id", Integer),
               #               Column("updated_at", DateTime),
               #               Column("modified_at", DateTime),
               Column("left_path", VARCHAR),
               Column("right_path", VARCHAR),
               #               Column("right_path_u_dec", VARCHAR),
               #               Column("parent_id", Integer),
               #               Column("cover", VARCHAR),
               #               Column("tag_artist_id", Integer),
               #               Column("tag_genre_id", Integer),
               #               Column("tag_title", VARCHAR),
               #               Column("tag_title_u_dec", VARCHAR),
               #               Column("tag_brainz_id", VARCHAR),
               #               Column("tag_year", Integer),
               )
tracks = Table("tracks", metadata,
               Column("id", Integer),
               Column("filename", VARCHAR),
               Column("album_id", Integer),
               #               Column("artist_id", Integer),
               )

playlists = Table("playlists", metadata,
                  Column("id", Integer),
                  Column("user_id", Integer),
                  Column("name", VARCHAR),
                  Column("items", VARCHAR),
                  )


def get_track(id):
    selection = select([tracks.c.album_id, tracks.c.filename]).where(tracks.c.id == id)
    track = conn.execute(selection).fetchone()
    return track


def get_path(id):
    selection = select([albums]).where(albums.c.id == id)
    album = conn.execute(selection).fetchone()
    path = album[1] + album[2] + '/'
    return path


def get_playlist():
    selection = select([playlists])
    playlist = conn.execute(selection).fetchall()
    for i in playlist:
        name = i[2]
        items = list(map(int, (i[3].split(','))))
        with open("m3u/" + str(name) + ".m3u", 'w') as m3u:
            for ii in items:
                track = get_track(ii)
                if track is None:
                    continue
                path = get_path(track[0]) + track[1]
                m3u.write(path + "\n")
        m3u.close


get_playlist()

