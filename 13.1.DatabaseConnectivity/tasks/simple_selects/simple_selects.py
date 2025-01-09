import sqlite3
import typing as tp


class DataBaseHandler:
    def __init__(self, sqlite_database_name: str):
        """
        Initialize all the context for working with database here
        :param sqlite_database_name: path to the sqlite3 database file
        """
        self.connection = sqlite3.connect(sqlite_database_name)
        self.cursor = self.connection.cursor()

    def get_most_expensive_track_names(self, number_of_tracks: int) -> tp.Sequence[tuple[str]]:
        """
        Return the sequence of track names sorted by UnitPrice descending.
        If the price is the same, sort by TrackId ascending.
        :param number_of_tracks: how many track names should be returned
        keywords: SELECT, ORDER BY, LIMIT
        :return:
        """
        query = """
        SELECT t.Name
        FROM Tracks t
        ORDER BY t.UnitPrice DESC, t.TrackId ASC
        LIMIT ?
        """
        self.cursor.execute(query, (number_of_tracks,))
        return self.cursor.fetchall()

    def get_tracks_of_given_genres(self, genres: tp.Sequence[str], number_of_tracks: int) -> tp.Sequence[tuple[str]]:
        """
        Return the sequence of track names that have one of the given genres
        sorted ascending by track duration and limit by number_of_tracks.
        :param number_of_tracks:
        :param genres:
        keywords: JOIN, WHERE, IN
        :return:
        """
        query = """
        SELECT t.Name
        FROM Tracks t
        JOIN Genres g ON t.GenreId = g.GenreId
        WHERE g.Name IN ({})
        ORDER BY t.Milliseconds ASC
        LIMIT ?
        """.format(','.join('?' for _ in genres))
        self.cursor.execute(query, (*genres, number_of_tracks))
        return self.cursor.fetchall()

    def get_tracks_that_belong_to_playlist_found_by_name(self, name_needle: str) -> tp.Sequence[tuple[str, str]]:
        """
        Return a sequence of track names and playlist names such that the track belongs to the playlist and
        the playlist's name contains `name_needle` (case sensitive).
        If the track belongs to more than one suitable playlist it
        should occur in the result for each playlist, but not just once.
        :param name_needle:
        keywords: JOIN, WHERE, LIKE
        :return:
        """
        try:
            query = """
            SELECT t.Name, p.Name
            FROM tracks t
            JOIN playlist_track pt ON t.Trackid = pt.TrackId
            JOIN playlists p ON pt.Playlistid = p.Playlistid
            WHERE p.Name LIKE ?
            """
            self.cursor.execute(query, ('%' + name_needle + '%',))
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")
            return []

    def teardown(self) -> None:
        """
        Cleanup everything after working with the database.
        Do anything that may be needed or leave blank.
        :return:
        """
        self.connection.close()
