from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pygame import mixer
from mutagen.mp3 import MP3
import os, random, time

# --------------------------------------------------------------------------
# Paths and constants
# --------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
os.chdir(BASE_DIR)  # Set the working directory to the script's location to ensure consistent file paths

# Initialize the Pygame mixer for audio playback
mixer.init()

# --------------------------------------------------------------------------
# Intro class for the main application intro screen
# --------------------------------------------------------------------------
class Intro:
    def __init__(self, root=None):
        self.root = root
        self.root.geometry('1024x600')  # Set window size
        self.root.iconbitmap('icons/Idrake ICO.ico')  # Set the window icon
        self.root.title('iDrake Player')  # Set the window title
        self.root.resizable(width=False, height=False)  # Make the window non-resizable

        self.frame = Frame(self.root)
        self.frame.pack()

        self.create()  # Call the method to set up the intro UI

    def create(self):
        # Create the background frame with a specified color
        self.ground = Frame(self.root, background=color_sx, width=1024, height=600)
        self.ground.place(x=0, y=0)

        # Load the image used for the intro button
        self.introI = PhotoImage(file='icons/logoIntro.png')

        # Create the intro button with the image
        self.buttonintro = Button(
            self.root,
            width=300,
            height=300,
            image=self.introI,
            background=color_sx,
            borderwidth=0,
            command=self.createWindow  # When clicked, go to the main window
        )
        self.buttonintro.place(x=350, y=130)

        # Initialize the main application window but don't show it yet
        self.window = MainWindow(master=self.root, intro=self)

    def createWindow(self):
        # Hide the intro frame and open the main app window
        self.frame.pack_forget()
        self.window.start_page()

class MainWindow:
    def __init__(self, master=None, intro=None):
        self.master = master
        self.intro = intro

        # List to store loaded music files
        self.music_list = []

        # Shuffle mode status and list
        self.shuffle_status = False
        self.shuffle_music_list = []

        # Playlist management
        self.playlist_music_list = []
        self.playlist_status = False
        self.playlist_file = str()

    def start_page(self):
        self.setup_background()
        self.create_buttons()
        self.create_main_ui()

    def setup_background(self):
        # Main background
        self.background = Frame(self.master, background=color_ground, width=1024, height=600)
        self.background.place(x=0, y=0)

        # Left sidebar
        self.sx = Frame(self.master, background=color_sx, width=120, height=600)
        self.sx.place(x=0, y=0)

        # Bottom bar
        self.under = Frame(self.master, background=color_under, width=1024, height=120, bd=0)
        self.under.place(x=0, y=480)

    def create_buttons(self):
        # Resume button
        self.resume = PhotoImage(file='icons/resume.png').subsample(2, 2)
        self.resumeButton = Button(self.under, width=32, height=32, image=self.resume, bg=color_under,
                                   highlightthickness=0, borderwidth=0, command=self.resume_music)
        self.resumeButton.place(x=490, y=15)

        # Pause button
        self.pause = PhotoImage(file='icons/pause.png').subsample(2, 2)
        self.pauseButton = Button(self.under, width=32, height=32, image=self.pause, bg=color_under,
                                  highlightthickness=0, borderwidth=0, command=self.pause_music)
        self.pauseButton.place(x=530, y=15)

        # Next song button
        self.next_icon = PhotoImage(file='icons/avantiDx.png').subsample(1, 1)
        self.nextButton = Button(self.under, width=28, height=27, image=self.next_icon, bg=color_under,
                                 highlightthickness=0, borderwidth=0, command=self.next_song)
        self.nextButton.place(x=585, y=16)

        # Previous song button
        self.prev_icon = PhotoImage(file='icons/avantiSx.png').subsample(1, 1)
        self.prevButton = Button(self.under, width=28, height=27, image=self.prev_icon, bg=color_under,
                                 highlightthickness=0, borderwidth=0, command=self.previous_song)
        self.prevButton.place(x=434, y=16)

        # Shuffle button
        self.shuffle = PhotoImage(file='icons/shuffle.png').subsample(1, 1)
        self.shuffleButton = Button(self.under, width=28, height=27, image=self.shuffle, bg=color_under,
                                    highlightthickness=0, borderwidth=0, command=self.shuffle_music)
        self.shuffleButton.place(x=680, y=16)

        # Import single song
        self.file = PhotoImage(file='icons/file.png').subsample(6, 6)
        self.fileButton = Button(self.sx, width=60, height=60, image=self.file, bg=color_sx,
                                 highlightthickness=0, borderwidth=0, command=lambda: self.selected(method=0))
        self.fileButton.place(x=29, y=110)

        # Import multiple songs
        self.files = PhotoImage(file='icons/files.png').subsample(6, 6)
        self.filesButton = Button(self.sx, width=60, height=60, image=self.files, bg=color_sx,
                                  highlightthickness=0, borderwidth=0, command=lambda: self.selected(method=1))
        self.filesButton.place(x=29, y=210)

        # Import folder
        self.folder = PhotoImage(file='icons/folder.png').subsample(6, 6)
        self.folderButton = Button(self.sx, width=62, height=50, image=self.folder, bg=color_sx,
                                   highlightthickness=0, borderwidth=0, command=lambda: self.selected(method=2))
        self.folderButton.place(x=29, y=310)

        # About/info button
        self.about_icon = PhotoImage(file='icons/info.png').subsample(8, 8)
        self.aboutButton = Button(self.background, image=self.about_icon, bg=color_ground,
                                  highlightthickness=0, width=42, height=42, command=self.about)
        self.aboutButton.place(x=962, y=8)

        # Delete buttons
        self.delete_song_btn = ttk.Button(self.background, text='Delete Selected', command=self.delete_song)
        self.delete_song_btn.place(x=160, y=440)

        self.delete_all_songs_btn = ttk.Button(self.background, text='Delete All', command=self.delete_all_songs)
        self.delete_all_songs_btn.place(x=300, y=440)

        # Extra: Play and Stop buttons
        self.play_btn = ttk.Button(self.background, text='Play', command=self.play)
        self.play_btn.place(x=160, y=400)

        self.stop_btn = ttk.Button(self.background, text='Stop', command=self.stop_music)
        self.stop_btn.place(x=300, y=400)

    def create_main_ui(self):
        # Main song list
        self.song_box = Listbox(self.background, bd=0, height=22, width=40, selectmode=SINGLE)
        self.song_box.place(x=150, y=25)

        # Scrollbar for song list
        self.scrollbar = ttk.Scrollbar(self.background)
        self.scrollbar.place(x=496, y=25, height=370)
        self.song_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.song_box.yview)

        # Playlist dropdown menu
        self.drop_list = ['Play playlist', 'Add selected song to playlist', 'Remove selected song from playlist',
                          'Remove all songs from playlist', 'Create and import new playlist',
                          'Import playlist', 'Export playlist']
        self.clicked = StringVar()
        self.drop = ttk.OptionMenu(self.background, self.clicked, 'Choose an option', *self.drop_list,
                                   command=self.drop_choice)
        self.drop.place(x=600, y=400)

        # Playlist song list
        self.playlist_song_box = Listbox(self.background, bd=0, height=22, width=40, selectmode=SINGLE)
        self.playlist_song_box.place(x=550, y=25)

        # Scrollbar for playlist
        self.playlist_scrollbar = ttk.Scrollbar(self.background)
        self.playlist_scrollbar.place(x=896, y=25, height=370)
        self.playlist_song_box.config(yscrollcommand=self.playlist_scrollbar.set)
        self.playlist_scrollbar.config(command=self.playlist_song_box.yview)

        # Currently playing song label
        self.current_play_song = Label(self.under, text='Now Playing: ', bd=0, relief=GROOVE, anchor=E)
        self.current_play_song.place(x=10, y=25)

        # Time indicators
        self.current_song_time = Label(self.under, text='--:--', bd=0, relief=GROOVE, anchor=E)
        self.current_song_time.place(x=304, y=70)

        self.total_song_time = Label(self.under, text='--:--', bd=0, relief=GROOVE, anchor=E)
        self.total_song_time.place(x=728, y=70)

        # Song progress slider
        self.my_slider = ttk.Scale(self.under, from_=0, to=100, orient=HORIZONTAL, value=0,
                                   command=self.slide, length=360)
        self.my_slider.place(x=350, y=70)

        # Volume control slider
        self.volume_slider = ttk.Scale(self.under, from_=0, to=1, orient=HORIZONTAL, value=1,
                                       command=self.volume, length=125)
        self.volume_slider.place(x=850, y=70)


    # Starts playback of the selected song from the position set by the slider
    def slide(self, x):
        selected_song_name = self.song_box.get(ACTIVE)
        if any(selected_song_name in i for i in self.music_list):
            song = [i for i in self.music_list if selected_song_name in i]
        mixer.music.load(song[0])
        mixer.music.play(loops=0, start=int(self.my_slider.get()))

    # Sets the volume based on the volume slider value
    def volume(self, x):
        mixer.music.set_volume(self.volume_slider.get())
        current_volume = mixer.music.get_volume()
        current_volume = current_volume * 100  # Volume percentage

    # Updates the playback time display every second
    def play_time(self):
        current_time = mixer.music.get_pos() / 1000
        converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

        # Choose the correct song source based on playlist status
        if self.playlist_status == False:
            self.selected_song_name = self.song_box.get(ACTIVE)
            if any(self.selected_song_name in i for i in self.music_list):
                song = [i for i in self.music_list if self.selected_song_name in i]
        elif self.playlist_status == True:
            self.selected_song_name = self.playlist_song_box.get(ACTIVE)
            if any(self.selected_song_name in i for i in self.playlist_music_list):
                song = [i for i in self.playlist_music_list if self.selected_song_name in i]

        song_mut = MP3(song[0])
        song_length = song_mut.info.length
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

        current_time += 1

        # Update slider and time labels
        if int(self.my_slider.get()) == int(song_length):
            self.current_song_time.config(text='00:00')
            self.total_song_time.config(text=converted_song_length)
        elif mixer.music.get_busy() == False:
            pass
        elif int(self.my_slider.get()) == int(current_time):
            slider_position = int(song_length)
            self.my_slider.config(to=slider_position, value=int(current_time))
        else:
            slider_position = int(song_length)
            self.my_slider.config(to=slider_position, value=int(self.my_slider.get()))
            converted_current_time = time.strftime('%M:%S', time.gmtime(int(self.my_slider.get())))
            self.current_song_time.config(text=converted_current_time)
            self.total_song_time.config(text=converted_song_length)
            next_time = int(self.my_slider.get()) + 1
            self.my_slider.config(value=next_time)

        # Call the function again after 1 second
        self.current_song_time.after(1000, self.play_time)

    # Handles the selected action from the dropdown menu
    def drop_choice(self, *args):
        if self.clicked.get() == self.drop_list[0]:
            self.play_playlist()
        elif self.clicked.get() == self.drop_list[1]:
            self.add_song_playlist()
        elif self.clicked.get() == self.drop_list[2]:
            self.delete_song_playlist()
        elif self.clicked.get() == self.drop_list[3]:
            self.delete_all_songs_playlist()
        elif self.clicked.get() == self.drop_list[4]:
            self.create_playlist()
        elif self.clicked.get() == self.drop_list[5]:
            self.import_playlist()
        elif self.clicked.get() == self.drop_list[6]:
            self.export_playlist()

    # Allows user to select music files (single, multiple, or folder)
    def selected(self, method=None):
        duplicate_music = False
        folder = None
        entry = None
        if method == 0:
            self.one_song = filedialog.askopenfilename(title='Choose a song', filetypes=(('mp3 Files', '*.mp3'), ))
            if self.one_song in self.music_list:
                warning_box = messagebox.askretrycancel(title='iDrake Player', message='Warning! The file already exists. Click Retry to select again or Cancel to stop.')
                if warning_box == True:
                    self.selected(method=0)
            elif self.one_song != '':
                self.music_list.append(self.one_song)
                music_name = os.path.split(self.one_song)[1].replace('.mp3', '')
                self.song_box.insert(END, music_name)

        elif method == 1:
            many_songs = filedialog.askopenfilenames(title='Choose many songs', filetypes=(('mp3 Files', '*.mp3'), ))
            for item in many_songs:
                if item in self.music_list:
                    duplicate_music = True
            if duplicate_music:
                duplicate_music = False
                warning_box = messagebox.askretrycancel(title='iDrake Player', message='Warning! Some files already exist. Click Retry to select again or Cancel to stop.')
                if warning_box == True:
                    self.selected(method=1)
            elif many_songs:
                for item in many_songs:
                    self.music_list.append(item)
                    music_name = os.path.split(item)[1].replace('.mp3', '')
                    self.song_box.insert(END, music_name)

        elif method == 2:
            folder = filedialog.askdirectory()
            for entry in os.listdir(folder):
                if any(os.path.split(entry)[1] in i for i in self.music_list):
                    duplicate_music = True
            if duplicate_music:
                duplicate_music = False
                warning_box = messagebox.askretrycancel(title='iDrake Player', message='Warning! Some files in the folder already exist. Click Retry to select again or Cancel to stop.')
                if warning_box == True:
                    self.selected(method=2)
            else:
                for entry in os.listdir(folder):
                    if entry.endswith('.mp3'):
                        music_path = folder + '/' + entry
                        self.music_list.append(music_path)
                        music_name = os.path.split(entry)[1].replace('.mp3', '')
                        self.song_box.insert(END, music_name)

    # Starts playing the selected song
    def play(self):
        self.playlist_status = False
        self.selected_song_name = self.song_box.get(ACTIVE)
        if self.shuffle_status == False:
            if any(self.selected_song_name in i for i in self.music_list):
                song = [i for i in self.music_list if self.selected_song_name in i]
        elif self.shuffle_status == True:
            if any(self.selected_song_name in i for i in self.shuffle_music_list):
                song = [i for i in self.music_list if self.selected_song_name in i]
        mixer.music.load(song[0])
        mixer.music.play(loops=0)
        self.current_play_song.config(text=f'Now playing: {self.selected_song_name}')
        self.play_time()

    # Resumes music if it's paused
    def resume_music(self):
        if mixer.music.get_busy() == False:
            mixer.music.unpause()

    # Pauses the currently playing music
    def pause_music(self):
        if mixer.music.get_busy() == True:
            mixer.music.pause()

    # Stops music playback and resets UI elements
    def stop_music(self):
        mixer.music.stop()
        self.current_play_song.config(text='Now playing: ')
        self.current_song_time.config(text='--:--')
        self.total_song_time.config(text='--:--')
        self.my_slider.config(value=0)

    # Toggles shuffle mode and rearranges the song list accordingly
    def shuffle_music(self):
        if self.shuffle_status == False:
            self.shuffle_status = True
            self.stop_music()
            self.shuffle_music_list.clear()
            self.shuffle_music_list = random.sample(self.music_list, len(self.music_list))
            self.song_box.delete(0, END)
            for item in self.shuffle_music_list:
                music_name = os.path.split(item)[1].replace('.mp3', '')
                self.song_box.insert(END, music_name)
        elif self.shuffle_status == True:
            self.shuffle_status = False
            self.stop_music()
            self.shuffle_music_list.clear()
            self.song_box.delete(0, END)
            for item in self.music_list:
                music_name = os.path.split(item)[1].replace('.mp3', '')
                self.song_box.insert(END, music_name)


    # Plays the previous song in the list
    def previous_song(self):
        self.my_slider.config(value=0)

        if self.playlist_status == False:
            next_one = self.song_box.curselection()
            next_one = next_one[0] - 1  # Move one song back
            song = self.song_box.get(next_one)
            self.current_play_song.config(text=f'Now playing: {song}')

            if self.shuffle_status == False:
                song = self.music_list[next_one]
            elif self.shuffle_status == True:
                song = self.shuffle_music_list[next_one]

            mixer.music.load(song)
            mixer.music.play(loops=0)

            self.song_box.selection_clear(0, END)
            self.song_box.activate(next_one)
            self.song_box.selection_set(next_one, last=None)

        elif self.playlist_status == True:
            next_one = self.playlist_song_box.curselection()
            next_one = next_one[0] - 1
            song = self.playlist_song_box.get(next_one)
            self.current_play_song.config(text=f'Now playing: {song}')
            song = self.playlist_music_list[next_one]

            mixer.music.load(song)
            mixer.music.play(loops=0)

            self.playlist_song_box.selection_clear(0, END)
            self.playlist_song_box.activate(next_one)
            self.playlist_song_box.selection_set(next_one, last=None)

    # Plays the next song in the list
    def next_song(self):
        self.my_slider.config(value=0)

        if self.playlist_status == False:
            next_one = self.song_box.curselection()
            next_one = next_one[0] + 1  # Move one song forward
            song = self.song_box.get(next_one)
            self.current_play_song.config(text=f'Now playing: {song}')

            if self.shuffle_status == False:
                song = self.music_list[next_one]
            elif self.shuffle_status == True:
                song = self.shuffle_music_list[next_one]

            mixer.music.load(song)
            mixer.music.play(loops=0)

            self.song_box.selection_clear(0, END)
            self.song_box.activate(next_one)
            self.song_box.selection_set(next_one, last=None)

        elif self.playlist_status == True:
            next_one = self.playlist_song_box.curselection()
            next_one = next_one[0] + 1
            song = self.playlist_song_box.get(next_one)
            self.current_play_song.config(text=f'Now playing: {song}')
            song = self.playlist_music_list[next_one]

            mixer.music.load(song)
            mixer.music.play(loops=0)

            self.playlist_song_box.selection_clear(0, END)
            self.playlist_song_box.activate(next_one)
            self.playlist_song_box.selection_set(next_one, last=None)

    # Deletes the currently selected song from the main list
    def delete_song(self):
        self.stop_music()
        for item in self.song_box.curselection():
            self.music_list.pop(item)
        self.song_box.delete(ACTIVE)

    # Deletes all songs from the main list
    def delete_all_songs(self):
        self.stop_music()
        self.song_box.delete(0, END)
        self.music_list.clear()


    # PLAYLIST FUNCTION

    # Creates a new playlist file and enables playlist mode
    def create_playlist(self):
        self.playlist_file = filedialog.asksaveasfilename(
            title='Create playlist',
            initialfile='Playlist.txt',
            defaultextension='.txt',
            filetypes=(('Text Documents', '*.txt'),)
        )
        self.playlist_status = True
        createPLfile = open(self.playlist_file, 'x')  # Create a new file
        createPLfile.close()

    # Adds the selected song to the playlist
    def add_song_playlist(self):
        self.selected_song_name = self.song_box.get(ACTIVE)
        if any(self.selected_song_name in i for i in self.music_list):
            song_full_path = [i for i in self.music_list if self.selected_song_name in i]
            song_full_path = str(song_full_path[0])
        if song_full_path not in self.playlist_music_list:
            self.playlist_status = True
            if self.playlist_file:
                with open(self.playlist_file, 'a+') as pf:
                    pf.write(f'{song_full_path}\n')  # Write song path to the playlist file
                self.playlist_music_list.append(song_full_path)
                music_name = os.path.split(song_full_path)[1].replace('.mp3', '')
                self.playlist_song_box.insert(END, music_name)
            else:
                messagebox.showwarning(
                    title='iDrake Player',
                    message='Warning! You must first create a TXT file using the proper button before adding songs to the playlist.'
                )
        else:
            messagebox.showwarning(
                title='iDrake Player',
                message='Warning! This song is already in the playlist. Please select another song.'
            )

    # Plays the selected song from the playlist
    def play_playlist(self):
        self.selected_song_name = self.playlist_song_box.get(ACTIVE)
        if any(self.selected_song_name in i for i in self.playlist_music_list):
            song = [i for i in self.playlist_music_list if self.selected_song_name in i]
        mixer.music.load(song[0])
        mixer.music.play(loops=0)
        self.current_play_song.config(text=f'Now playing: {self.selected_song_name}')
        self.play_time()

    # Imports a playlist from an existing TXT file
    def import_playlist(self):
        self.playlist_file = filedialog.askopenfilename(
            title='Import playlist',
            filetypes=(('txt Files', '*.txt'),)
        )
        self.playlist_status = True
        with open(self.playlist_file, 'r') as pf:
            for line in pf:
                x = line[:-1]  # Remove newline character
                self.playlist_music_list.append(x)
                music_name = os.path.split(line)[1].replace('.mp3\n', '')
                self.playlist_song_box.insert(END, music_name)

    # Exports the current playlist to a new TXT file
    def export_playlist(self):
        if self.playlist_music_list:
            export_pl_path = filedialog.asksaveasfilename(
                title='Export playlist',
                initialfile='Playlist.txt',
                defaultextension='.txt',
                filetypes=(('Text Documents', '*.txt'),)
            )
            createExportPLfile = open(export_pl_path, 'x')  # Create the export file
            createExportPLfile.close()
            with open(export_pl_path, 'w') as pl_export_file:
                for item in self.playlist_music_list:
                    pl_export_file.write(f'{item}\n')
        else:
            messagebox.showwarning(
                title='iDrake Player',
                message='Warning! You are trying to export an empty playlist. Please add at least one song before exporting.'
            )

    # Deletes the selected song from the playlist
    def delete_song_playlist(self):
        self.stop_music()
        for item in self.playlist_song_box.curselection():
            self.playlist_music_list.pop(item)
        with open(self.playlist_file, 'r+') as pf:
            lines = pf.readlines()
            pf.seek(0)
            pf.truncate()
            for number, line in enumerate(lines):
                if number not in [item]:
                    pf.write(line)
        self.playlist_song_box.delete(ACTIVE)

    # Deletes all songs from the playlist
    def delete_all_songs_playlist(self):
        self.stop_music()
        self.playlist_status = False
        self.playlist_song_box.delete(0, END)
        self.playlist_music_list.clear()
        file = open(self.playlist_file, 'w')  # Overwrite with an empty file
        file.close()



    # Displays the About window with app information
    def about(self):
        messagebox.showinfo(
            title='About iDrake Player',
            message='''iDrake Player is a cross-platform MP3 audio file player entirely written in Python by:
    - De Vivo Damiano;
    - Locatelli Federico;
    - Oltrecolli Matteo.

iDrake Player is built using the following libraries:
    - Tkinter (for the GUI, file/folder dialog windows, and message boxes to notify the user when needed);
    - Pygame (specifically mixer.music to handle audio files);
    - Mutagen (to retrieve information from MP3 files);
    - OS (to manage file paths and search for MP3 files within a folder);
    - Random (to manage shuffle playback mode);
    - Time (allows the playback timeline to function properly).

iDrake Player v1.0''')

# GUI color theme variables
color_ground = '#121212'
color_under = '#000000'
color_sx = '#181818'

# Starts the application
if __name__ == '__main__':
    root = Tk()
    intro = Intro(root)
    root.mainloop()
