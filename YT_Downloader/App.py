from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import events
import static
import utils

# Must be global
is_audio_selected = None
is_only_audio_selected = None

"""
All widgets from GUI are created and placed in that class. It includes also important variables which must be here.
For example dictionary of all widgets in app. 
"""


class App(Frame):
    widgets = {}
    is_url_valid = False
    is_name_valid = False
    is_path_valid = False

    def __init__(self, master):
        super().__init__(master=master)
        self.master = master

        global is_audio_selected, is_only_audio_selected
        is_audio_selected = BooleanVar(self.master)
        is_only_audio_selected = BooleanVar(self.master)

        self.widgets.update({"master": master})
        self.__change_meta_data()
        self.__set_config_settings()
        self.__create_widgets()

    def __change_meta_data(self):
        """
        Function changes meta data of program.
        """
        self.__set_title()
        self.__set_icon()

    def __set_config_settings(self):
        """
        Function sets basic settings of program.
        """
        self.master.geometry(static.DEFAULT_SIZE_OF_FRAME)
        self.master.configure(bg=static.DEFAULT_COLOR)

    def __create_widgets(self):
        """
        Function creates widgets which are visible from the start of the program.
        """
        self.__create_and_place_logo_label(static.PATH_TO_LOGO)
        self.__create_and_place_thumbnail_section()
        self.__create_and_place_url_section()
        self.__create_and_place_name_section()
        self.__create_and_place_loc_section()
        self.__create_and_place_download_btn()
        self.__create_and_place_audio_check_buttons()

    def __set_title(self):
        """
        Function sets the title of the program which is visible in left upper corner of the frame.
        """
        self.master.title(static.APP_TITLE)

    def __set_icon(self):
        """
        Function sets the icon of program which is visible in left upper corner of the frame.
        """
        self.master.iconbitmap(static.PATH_TO_ICON)

    def __create_and_place_logo_label(self, image_path):
        """
        Function creates and places label widget which will contain logo of the app. Image which will be logo will be
        resized before.
        :param image_path: Path to the image which will be logo.
        """
        logo = Image.open(image_path)
        resized_logo = utils.resize_image(logo, static.DEFAULT_LOGO_SIZE)
        logo = ImageTk.PhotoImage(resized_logo)  # must convert to PhotoImage, because image passed to Label cannot
        # be Image type
        logo_label = Label(self.master, image=logo, bg=static.DEFAULT_COLOR)
        logo_label.image = logo  # that is necessary because of Tk problems
        self.widgets.update({"logo_label": logo_label})
        self.__place_logo_label(logo_label)


    @staticmethod
    def __place_logo_label(logo_label):
        """
        Function places logo_label in appropriate place.
        :param logo_label: Label widget which contains logo of the app
        """
        logo_label.place(relwidth=1, relheight=0.15, y=10)


    def __create_and_place_thumbnail_section(self):
        """
        Function creates and places two label widgets. One of them will contain thumbnail of the video, second one
        will contain title of the video. Their contents are not visible from the start.
        """
        thumbnail_label = Label(self.master, image=None, bg=static.DEFAULT_COLOR)  # image is not displayed from the
        # start
        thumbnail_label.image = None  # that is necessary because of Tk problems
        title_label = Label(self.master, text="", fg="white", bg=static.DEFAULT_COLOR,
                            font=static.DEFAULT_FONT)  # title is not displayed as well
        self.widgets.update({"thumbnail_label": thumbnail_label})
        self.widgets.update({"title_label": title_label})
        self.__place_thumbnail_section(thumbnail_label, title_label)


    @staticmethod
    def __place_thumbnail_section(thumbnail_label, title_label):
        """
        Function places thumbnail_label and title_label in appropriate places.
        :param thumbnail_label: Label widget which contains thumbnail of the video
        :param title_label: Label widget which contains title of the video
        """
        thumbnail_label.place(relwidth=0.33, relheight=0.3, y=20, relx=0.33, rely=0.15)
        title_label.place(relwidth=1, relheight=0.05, y=30, rely=0.45)


    def __create_and_place_url_section(self):
        """
        Function creates and places label widget and entry widget. Label widget contains short text "URL: ".
        Entry widget will allow user to input URL address. Entry widget will have assigned function which will trace
        every change in user input.
        """
        url_label = Label(self.master, text="URL: ", fg="white", bg=static.DEFAULT_COLOR, font=static.DEFAULT_FONT)
        url = StringVar()
        url.trace("w", lambda name, index, mode, url=url: events.change_url_input_color_and_update_basic_info(url, self,
                                                "green"))  # it allows to follow every change in URL given by user
        url_input = Entry(self.master, cursor="xterm", fg="white", bg=static.DEFAULT_COLOR, borderwidth=2,
                          relief="solid", font=static.DEFAULT_FONT, textvariable=url)
        self.widgets.update({"url_label": url_label})
        self.widgets.update({"url_input": url_input})
        self.__place_url_section(url_label, url_input)


    @staticmethod
    def __place_url_section(url_label, url_input):
        """
        Function places url_label and url_input in appropriate places.
        :param url_label: Label widget containing short text "URL: "
        :param url_input: Entry widget which allows user to input URL address
        """
        url_label.place(relwidth=0.1, relheight=0.05, relx=0.1, rely=0.62)
        url_input.place(relwidth=0.6, relheight=0.05, relx=0.21, rely=0.62)


    def __create_and_place_name_section(self):
        """
        Function creates and places label widget and entry widget. Label widget contains short text "Nazwa: ".
        Entry widget will allow user to input name of the downloaded file. Entry widget will have assigned function
        which will trace every change in user input.
        """
        name_label = Label(self.master, text="Nazwa:", fg="white", bg=static.DEFAULT_COLOR, font=static.DEFAULT_FONT)
        file_name = StringVar()
        file_name.trace("w", lambda name, index, mode, file_name=file_name:
                        events.change_name_input_color(file_name, self, "green"))  # it allows to follow every change in
        # name given by user
        name_input = Entry(self.master, cursor="xterm", fg="white", bg=static.DEFAULT_COLOR, borderwidth=2,
                           relief="solid", font=static.DEFAULT_FONT, textvariable=file_name)
        self.widgets.update({"name_label": name_label})
        self.widgets.update({"name_input": name_input})
        self.__place_name_section(name_label, name_input)

    @staticmethod
    def __place_name_section(name_label, name_input):
        """
        Function places name_label and name_input in appropriate places.
        :param name_label: Label widget which contains short text "Nazwa: ".
        :param name_input: Entry widget which allows user to input name of the downloaded file.
        """
        name_label.place(relwidth=0.1, relheight=0.05, relx=0.1, rely=0.72)
        name_input.place(relwidth=0.6, relheight=0.05, relx=0.21, rely=0.72)

    def __create_and_place_loc_section(self):
        """
        Function creates and places label widget, entry widget and button widget. Label widget contains short text
        "Zapisz do: ". Entry widget will allow user to input path to the folder where downloaded file will be saved.
        Entry widget will have assigned function which will trace every change in user input. Button widget will allow
        to choose path of that folder in an easier way.
        """
        loc_label = Label(self.master, text="Zapisz do:", fg="white", bg=static.DEFAULT_COLOR, font=static.DEFAULT_FONT)
        location_path = StringVar()
        location_path.trace("w", lambda name, index, mode, location_path=location_path: events.change_loc_input_color
                            (location_path, self, "green"))  # it allows to follow every change in location(path)
        # given by user
        loc_input = Entry(self.master, cursor="xterm", fg="white", bg=static.DEFAULT_COLOR, borderwidth=2,
                          relief="solid", font=static.DEFAULT_FONT, textvariable=location_path)
        loc_button = Button(self.master, text="...", fg="white", bg=static.DEFAULT_COLOR, borderwidth=2, relief="solid",
                            cursor="hand2", command=self.__choose_loc, font=static.DEFAULT_FONT)
        self.widgets.update({"loc_label": loc_label})
        self.widgets.update({"loc_input": loc_input})
        self.widgets.update({"loc_button": loc_button})
        self.__place_loc_section(loc_label, loc_input, loc_button)


    @staticmethod
    def __place_loc_section(loc_label, loc_input, loc_button):
        """
        Function places loc_label, loc_input and loc_button in appropriate places.
        :param loc_label: Label widget which contains short text "Zapisz do: ".
        :param loc_input: Entry widget which allows user to input path to the folder where downloaded file will be saved
        :param loc_button: Button widget which allows to choose path of folder where downloaded file will be saved
        in an easier way.
        """
        loc_label.place(relwidth=0.1, relheight=0.05, relx=0.1, rely=0.82)
        loc_input.place(relwidth=0.6, relheight=0.05, relx=0.21, rely=0.82)
        loc_button.place(relwidth=0.05, relheight=0.05, relx=0.82, rely=0.82)


    def __create_and_place_download_btn(self):
        """
        Function creates and places button widget. Button widget will allow to start downloading.
        """
        download_btn = Button(self.master, text="Pobierz", fg="white", bg=static.DEFAULT_COLOR,
                              activebackground=static.FOCUS_ON_BTN_COLOR, borderwidth=2, relief="solid", cursor="hand2",
                              font=static.DEFAULT_FONT, command=events.download_video)
        self.widgets.update({"download_btn": download_btn})
        self.__place_download_btn(download_btn)

    @staticmethod
    def __place_download_btn(download_btn):
        """
        Function places download_btn in appropriate place.
        :param download_btn: Button widget which allows to start downloading.
        """
        download_btn.place(relwidth=0.16, relheight=0.08, relx=0.42, rely=0.9)

    def __create_and_place_audio_check_buttons(self):
        """
        Function creates and places two check button widgets. First of them tells whether downloading video will contain
        audio. Second one tells whether downloading video will contain only audio.
        """
        global is_audio_selected, is_only_audio_selected
        is_audio_checkbutton = Checkbutton(self.master, text="Dźwięk", fg="black", bg=static.DEFAULT_COLOR,
                        onvalue=True, offvalue=False, variable=is_audio_selected,
                        command=events.set_properly_other_check_buttons_and_update_quality_list)
        is_audio_checkbutton.select()  # we want audio checkbutton to be selected from the beginning
        is_only_audio_check_button = Checkbutton(self.master, text="Tylko dźwięk", fg="black", bg=static.DEFAULT_COLOR,
                                                onvalue=True, offvalue=False, variable=is_only_audio_selected,
                                                command=events.select_audio_check_button_and_update_quality_menubutton)
        self.widgets.update({"is_audio_check_button": is_audio_checkbutton})
        self.widgets.update({"is_only_audio_check_button": is_only_audio_check_button})
        self.__place_check_buttons(is_audio_checkbutton, is_only_audio_check_button)

    @staticmethod
    def __place_check_buttons(is_audio_checkbutton, is_only_audio_check_button):
        """
        Function places is_audio_checkbutton and is_only_audio_check_button in appropriate places.
        :param is_audio_checkbutton: Check button widget which tells whether downloading video will contain audio
        :param is_only_audio_check_button: Check button widget which tells whether downloading video will contain only
        audio
        """
        is_audio_checkbutton.place(relwidth=0.12, relheight=0.06, relx=0.62, rely=0.91)
        is_only_audio_check_button.place(relwidth=0.12, relheight=0.06, relx=0.75, rely=0.91)

    def __choose_loc(self):
        """
        Function opens GUI which allows to choose folder where downloaded video will be saved.
        """
        loc_to_folder = filedialog.askdirectory()
        loc_input = self.widgets.get("loc_input")
        loc_input.delete(0, END)  # delete actual input
        loc_input.insert(0, loc_to_folder)  # insert to input label chosen from dialog
