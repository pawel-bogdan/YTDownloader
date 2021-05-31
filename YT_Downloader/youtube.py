import requests
from pytube import YouTube
from PIL import Image, ImageTk
import utils
import static
import io
import events


"""
Class responsible for connecting with Youtube, downloading data.
"""


class YTVideo:
    def __init__(self, url):
        self.__yt = YouTube(url)
        self.__url = url


    @property
    def title(self):
        """
        The property that returns the title of the video.
        :return: String which contains title of video.
        """
        return self.__yt.title

    @property
    def thumbnail(self):
        """
        The property that returns the thumbnail of the video. Thumbnail is resized and casted to PhotoImage type.
        :return: Resized and casted to PhotoImage type thumbnail.
        """
        thumbnail_in_bytes = requests.get(self.__yt.thumbnail_url).content
        thumbnail = Image.open(io.BytesIO(thumbnail_in_bytes))
        resized_thumbnail = utils.resize_image(thumbnail, static.DEFAULT_THUMBNAIL_SIZE)
        thumbnail = ImageTk.PhotoImage(resized_thumbnail)
        return thumbnail

    def get_available_resolutions(self, is_audio, is_only_audio):
        """
        Function searches for available resolutions.
        :param is_audio: Boolean value which tells whether file must include audio.
        :param is_only_audio: Boolean value which tells whether file must include only audio(without video).
        :return: List of all available resolutions.
        """
        resolutions = []
        if is_audio and not is_only_audio:
            streams = self.__yt.streams.filter(progressive=True).desc()
        elif is_only_audio:
            streams = self.__yt.streams.filter(only_audio=True).desc()
        else:
            streams = self.__yt.streams.filter(only_video=True).asc()

        for vid in streams:
            if vid.resolution not in resolutions:
                resolutions.append(vid.resolution)

        if None in resolutions:
            resolutions.remove(None)  # None is related to "automatic" resolution in Youtube. We delete it.
        return resolutions

    def download(self, filename, path, resolution, is_audio, is_only_audio):
        """
        Function downloads file in selected options and save it in chosen folder.
        :param filename: Name under which file will be saved.
        :param path: Path to the folder where file will be saved.
        :param resolution: Resolution in which will be downloaded video.
        :param is_audio: Boolean value which tells whether file must include audio.
        :param is_only_audio: Boolean value which tells whether file must include only audio(without video).
        """
        if is_only_audio:  # it must be divided on if/elif/else
            video_to_download = self.__yt.streams.filter(only_audio=is_only_audio).first()
        elif not is_audio:
            video_to_download = self.__yt.streams.filter(resolution=resolution, only_video=True).first()
        else:
            video_to_download = self.__yt.streams.filter(resolution=resolution, progressive=True).first()

        if video_to_download is not None:
            try:
                events.create_download_started_dialog()
                video_to_download.download(filename=filename, output_path=path)
                events.create_download_finished_dialog()
            except KeyError:
                events.create_download_error_dialog("Podany adres odnosi się do transmisji na żywo")
        else:
            events.create_download_error_dialog("Pobieranie jest niemożliwe.")

    def is_available(self):
        """
        Function checks availability of video.
        """
        self.__yt.check_availability()

    def get_url(self):
        """
        Function returns URL address of video.
        :return: URL address of video
        """
        return self.__url
