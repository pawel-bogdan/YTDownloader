import re
from os import path
import youtube as yt
from pytube import exceptions as exc
"""
Validating methods available here.
"""


def validate_url(url):
    """
    Function validates URL address.
    :param url: StringVar which contains URL address
    :return: Boolean value. True if url has been validated properly. False if not.
    """
    url = url.get()
    yt_video_url_pattern = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$"
    if re.match(yt_video_url_pattern, url) is None:
        return False
    try:
        video = yt.YTVideo(url)
        video.is_available()
    except (exc.RegexMatchError, exc.VideoUnavailable, exc.VideoPrivate, exc.MembersOnly, exc.RecordingUnavailable,
            exc.VideoRegionBlocked):
        return False
    return True


def validate_name(name):
    """
    Function validates name under which user wants to save video.
    :param name: StringVar which contains name under which user wants to save video.
    :return: Boolean value. True if name has been validated properly. False if not.
    """
    forbidden_chars = {"\\", "/", ":", "*", "?", "\"", "<", ">", "|"}
    name = name.get()
    if name == "":
        return False
    for char in name:
        if char in forbidden_chars:
            return False
    return True


def validate_location(location):
    """
    Function validates path to location where user wants to save video.
    :param location: StringVar which contains path to folder where user wants to save video.
    :return: Boolean value. True if path has been validated properly. False if not.
    """
    return path.isdir(location.get())
