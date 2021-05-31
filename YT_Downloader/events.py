from tkinter import Menubutton, Menu, messagebox
import validator
import static
import App
import youtube as yt

"""
All events available here.
"""

actual_video = None
marked_resolution = None


def change_url_input_color_and_update_basic_info(url, frame, color):
    """
    Function changes color of url entry widget. It depends on situation on which. If url is validated - background of
    url entry widget is "color" otherwise is in default color. It also shows basic info like thumbnail, title and
    available resolutions of video(if validated properly). This function updates variables like actual_video and
    is_url_valid.
    :param url: StringVar which contains URL address
    :param frame: frame which will be updated
    :param color: color on which background of url entry widget will be changed if url will be valid
    """
    global actual_video
    url_input = frame.widgets.get("url_input")
    if validator.validate_url(url):
        App.App.is_url_valid = True
        url_input.configure(bg=color)
        if actual_video is None:
            actual_video = yt.YTVideo(url.get())
            show_video_info()
            if not App.is_only_audio_selected.get():
                create_quality_menubutton()
                update_resolutions_list()
        elif url.get().find(actual_video.get_url()) == -1:  # if url contains primary video url, it still works.
            # repeated code just for efficiency
            actual_video = yt.YTVideo(url.get())
            show_video_info()
            if not App.is_only_audio_selected.get():
                create_quality_menubutton()
                update_resolutions_list()
    else:
        url_input.configure(bg=static.DEFAULT_COLOR)
        hide_title()
        hide_thumbnail()
        destroy_quality_menubutton()
        App.App.is_url_valid = False
        actual_video = None


def change_name_input_color(name, frame, color):
    """
    Function changes color of name entry widget. It depends on situation on which. If name is validated - background of
    name entry widget is "color" otherwise is in default color. This function updates variable is_name_valid.
    :param name: StringVar which contains name under which user wants to save file
    :param frame: frame which will be updated
    :param color: color on which background of name entry widget will be changed if name will be valid
    """
    name_input = frame.widgets.get("name_input")
    if validator.validate_name(name):
        App.App.is_name_valid = True
        name_input.configure(bg=color)
    else:
        name_input.configure(bg=static.DEFAULT_COLOR)
        App.App.is_name_valid = False


def change_loc_input_color(location, frame, color):
    """
    Function changes color of location entry widget. It depends on situation on which. If location is validated -
    background of location entry widget is "color" otherwise is in default color. This function updates variable
    is_path_valid.
    :param location: StringVar which contains path to folder where user wants to save video.
    :param frame: frame which will be updated
    :param color: color on which background of name entry widget will be changed if location will be valid
    """
    loc_input = frame.widgets.get("loc_input")
    if validator.validate_location(location):
        App.App.is_path_valid = True
        loc_input.configure(bg=color)
    else:
        loc_input.configure(bg=static.DEFAULT_COLOR)
        App.App.is_path_valid = False


def change_download_btn_color():
    """
    Function changes download button color.
    """
    download_btn = App.App.widgets.get("download_btn")
    download_btn.configure(bg=static.FOCUS_ON_BTN_COLOR)


def download_video():
    """
    Functions tries to start downloading. If downloading is impossible(some of necessary input is not valid), non valid
    inputs are marked on red color.
    """
    name_input = App.App.widgets.get("name_input")
    loc_input = App.App.widgets.get("loc_input")
    name = name_input.get()
    path_to_save = loc_input.get()
    if App.App.is_url_valid and App.App.is_name_valid and App.App.is_path_valid and \
            (marked_resolution is not None or App.is_only_audio_selected):
        is_audio_selected = App.is_audio_selected.get()
        is_only_audio_selected = App.is_only_audio_selected.get()
        actual_video.download(name, path_to_save, marked_resolution, is_audio_selected, is_only_audio_selected)
    else:
        change_color_for_non_valid_inputs()


def change_color_for_non_valid_inputs():
    """
    Function changes color on red for non valid inputs.
    """
    if not App.App.is_url_valid:
        mark_widget_input_as_invalid(App.App.widgets.get("url_input"))
    if not App.App.is_name_valid:
        mark_widget_input_as_invalid(App.App.widgets.get("name_input"))
    if not App.App.is_path_valid:
        mark_widget_input_as_invalid(App.App.widgets.get("loc_input"))
    if marked_resolution is None:
        quality_menubutton = App.App.widgets.get("quality_menubutton")
        if quality_menubutton is not None:
            mark_widget_input_as_invalid(quality_menubutton)


def show_video_info():
    """
    Function shows basic video info like thumbnail and title.
    """
    display_thumbnail()
    display_title()


def display_thumbnail():
    """
    Function displays thumbnail.
    """
    thumbnail_label = App.App.widgets.get("thumbnail_label")
    image = actual_video.thumbnail
    thumbnail_label.configure(image=image)
    thumbnail_label.image = image


def display_title():
    """
    Function displays title.
    """
    title_label = App.App.widgets.get("title_label")
    title_label.configure(text=actual_video.title)


def hide_title():
    """
    Function hides title.
    """
    title_label = App.App.widgets.get("title_label")
    title_label.configure(text="")


def hide_thumbnail():
    """
    Function hides thumbnail.
    """
    thumbnail_label = App.App.widgets.get("thumbnail_label")
    thumbnail_label.configure(image=None)
    thumbnail_label.image = None


def create_quality_menubutton():
    """
    Function creates and places quality menu button widget.
    """
    quality_menubutton = Menubutton(App.App.widgets.get("master"), text="Jakość", cursor="hand2", fg="white",
                                    bg=static.DEFAULT_COLOR, font=static.DEFAULT_FONT, borderwidth=2, relief="solid")
    quality_menubutton.menu = Menu(quality_menubutton, tearoff=0)  # creating Menu without first element which is line
    quality_menubutton["menu"] = quality_menubutton.menu  # must stay, because of Tk problems
    App.App.widgets.update({"quality_menubutton": quality_menubutton})
    place_quality_menubutton(quality_menubutton)


def destroy_quality_menubutton():
    """
    Function destroys quality menu button widget.
    """
    quality_menubutton = App.App.widgets.get("quality_menubutton")
    if quality_menubutton is not None:  # if quality_menubutton does not exist we do not destroy it
        quality_menubutton.destroy()
        App.App.widgets.pop("quality_menubutton")
    global marked_resolution
    marked_resolution = None


def place_quality_menubutton(quality_menu_btn):
    """
    Function places quality_menu_btn in appropriate place.
    :param quality_menu_btn: Menu button widget which contains all available qualities/resolutions
    """
    quality_menu_btn.place(relwidth=0.1, relheight=0.05, relx=0.82, rely=0.62)


def update_resolutions_list():
    """
    Function updates resolutions list widget. Every update is preceded by reset(destroying and creating) quality
    menu button.
    """
    # firstly we need to reset actual resolutions list
    if actual_video is None:  # situation when url is not pasted
        return
    destroy_quality_menubutton()
    create_quality_menubutton()
    quality_menubutton = App.App.widgets.get("quality_menubutton")
    is_audio = App.is_audio_selected.get()
    is_only_audio = App.is_only_audio_selected.get()
    available_quality = actual_video.get_available_resolutions(is_audio, is_only_audio)

    # arguments for save_marked_resolution must be constant, it cannot be "i" instead of "144p" or "360p"
    for i in available_quality:
        if i == "144p":
            quality_menubutton.menu.add_radiobutton(label=i, command=lambda: save_marked_resolution("144p"))
        elif i == "240p":
            quality_menubutton.menu.add_radiobutton(label=i, command=lambda: save_marked_resolution("240p"))
        elif i == "360p":
            quality_menubutton.menu.add_radiobutton(label=i, command=lambda: save_marked_resolution("360p"))
        elif i == "480p":
            quality_menubutton.menu.add_radiobutton(label=i, command=lambda: save_marked_resolution("480p"))
        elif i == "720p":
            quality_menubutton.menu.add_radiobutton(label=i, command=lambda: save_marked_resolution("720p"))
        elif i == "1080p":
            quality_menubutton.menu.add_radiobutton(label=i, command=lambda: save_marked_resolution("1080p"))


def save_marked_resolution(res):
    """
    Function updates global variable marked_resolution.
    :param res: value which will be assigned to marked_resolution
    """
    global marked_resolution
    marked_resolution = res
    quality_menubutton = App.App.widgets.get("quality_menubutton")
    quality_menubutton.configure(bg="green")



def select_audio_check_button_and_update_quality_menubutton():
    """
    This function is an event on toggling "is only audio". It also updates quality_menubutton.
    """
    select_audio_check_button()
    if App.is_only_audio_selected.get():
        destroy_quality_menubutton()
    elif actual_video is not None:
        create_quality_menubutton()
        update_resolutions_list()


def set_properly_other_check_buttons_and_update_quality_list():
    """
    This function is an event on deselecting "is audio" check button. If "is audio" check button is deselected,
    "is only audio" button is also deselected. It also updates resolutions list.
    """
    if not App.is_audio_selected.get():
        is_only_audio_check_button = App.App.widgets.get("is_only_audio_check_button")
        is_only_audio_check_button.deselect()
    update_resolutions_list()


def select_audio_check_button():
    """
    Function selects "is audio" check button.
    """
    App.App.widgets.get("is_audio_check_button").select()


def mark_widget_input_as_invalid(widget):
    """
    Function sets background color on red, for given widget.
    :param widget: widget which will have change background color
    """
    widget.configure(bg="red")


def create_download_error_dialog(description):
    """
    Function creates error window dialog window with given description.
    :param description: text which will be included into window dialog
    """
    messagebox.showerror("Błąd pobierania", "Nie można pobrać podanego filmu. {0}".format(description))


def create_download_finished_dialog():
    """
    Function creates window dialog window with information that downloading has ended.
    """
    messagebox.showinfo("Info", "Pobieranie zakończone.")


def create_download_started_dialog():
    """
    Function creates window dialog window with information that downloading has started.
    """
    messagebox.showinfo("Info", "Pobieranie rozpoczęte.")
