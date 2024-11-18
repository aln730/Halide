"""
Author: zxcv@csh/asg7201
Description: CLI-based Music player using Python3, PyGame, Random, OS
PS: Don't mind some of the the crappy code. 
TM: expand the music library and add an option to create playlists.
"""
import os
import pygame
from colorama import init, Fore
from termcolor import colored

init()

class MusicPlayer:
    def __init__(self):
        self.songs = []
        self.current_song_index = 0
        self.paused = False
        self.folder_path = ''
        pygame.init()
        pygame.mixer.init()

    def read_songs_from_folder(self, folder_path):
        self.folder_path = folder_path
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp3"):
                self.songs.append(os.path.join(folder_path, filename))

    def list_songs(self):
        print("Available songs:")
        for i, song in enumerate(self.songs):
            print(f"{i+1}. {song}")

    def play_song(self, song_index):
        if song_index.isdigit() and 0 <= int(song_index) - 1 < len(self.songs):
            pygame.mixer.music.load(self.songs[int(song_index) - 1])
            pygame.mixer.music.play()
            self.current_song_index = int(song_index) - 1
        else:
            print("Invalid song index.")

    def pause_song(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
        else:
            pygame.mixer.music.unpause()
            self.paused = False

    def stop_song(self):
        pygame.mixer.music.stop()

    def next_song(self):
        if len(self.songs) > 1:
            self.current_song_index += 1
            if self.current_song_index >= len(self.songs):
                self.current_song_index = 0
            self.play_song(str(self.current_song_index + 1))

    def previous_song(self):
        if len(self.songs) > 1:
            self.current_song_index -= 1
            if self.current_song_index < 0:
                self.current_song_index = len(self.songs) - 1
            self.play_song(str(self.current_song_index + 1))

    def seek_song(self, seconds):
        pygame.mixer.music.set_pos(seconds)

    def shuffle_songs(self):
        import random
        random.shuffle(self.songs)
        self.play_song("1")

    def run(self):
        print("CLIotify - root@zxcv\n")
        ascii ="""⠀⠀⠀⠀⠀⠀⠀⠀⣾⣛⡿⡿⢽⣶⣤⣀⣀⣀⣀⣀⣀⣠⣴⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⢬⡭⢭⣭⣽⣗⡋⠈⠉⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡞⠁⣂⡠⠾⢛⣛⣀⣀⠀⠀⠙⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣟⠛⠃⡀⣀⡉⠀⠄⠄⠈⠉⠑⠢⣄⡉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠈⠲⣍⣿⣿⣿⣿⣿⣿⣿⡉⠛⢿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⢿⣿⣖⠿⣯⢆⠀⠀⢁⠞⠉⠙⠻⠿⣿⣿⣿⣿⣦⣀⣩⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣤⡄⠀⠀⠀⢀⡴⠛⢓⡜⢿⣿⣆⢀⢿⠀⠀⢻⣄⡀⠀⠀⠀⢒⣛⣫⣿⡟⠻⢿⠿⣾⡻⣿⡆⠀⠀⠀⠀⠀⠀⠀
⢀⡀⢤⣤⢾⣿⣷⠄⢀⡠⠈⣄⠤⠀⠛⢾⣿⣿⣾⡎⠀⠀⠀⠈⠛⠒⠀⠀⠀⠀⠀⢈⣑⡒⠤⠄⣀⣈⣭⠗⠀⠀⠀⠀⠀⠀⠀
⡏⠈⠉⠉⣿⣿⣿⠍⠹⣿⡄⠉⠻⢶⣌⠀⠻⣿⣿⣿⣷⣶⣴⣾⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣦⣄⣒⣊⠀⠀⠀⠀⠀⠀⠀⠀
⠹⡦⡁⠀⠸⡟⣿⣤⢬⢿⠀⠀⠀⠀⠉⡷⣄⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣶⣤⣤⣀⠀⠀
⠀⠙⢾⡴⠄⡀⢸⣿⡏⠁⠀⠀⠀⠀⠀⠈⠪⡓⢤⡈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣿⣟⢵⣆⣈⣍⣿⣿⣿⣿⣷⡄
⠀⠀⠀⢷⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠈⠂⢌⡓⠢⢤⣉⠉⠛⠻⢿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⠿⠛⠛⠛⠛⢛⣨⣿⡗
⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠲⠤⠍⣒⡂⠀⢼⡉⠛⠁⠀⠀⠀⣠⠟⠻⠙⠉⠀⠁⣉⣁⡠⠔⠀
⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠒⡇⠀⠀⠀⠀⠈⢀⡠⠔⠒⠀⠉⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢹⡘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⡿⣕⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⠤⠄⠰⠤⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢳⡎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣺⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⣿⣾⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡶⠏⠉⠻⢿⣿⣿⣿⣿⣿⡷⠆⠙⠿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⣄⠀⠀⠀⠈⣛⣿⡿⠟⢿⣷⣮⣸⡐⠛⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠙⠯⢒⣲⠄⠀⠀⠀⢄⣠⠀⠈⠿⣿⡀⠀⢻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠐⠲⢌⣓⠤⣀⠀⠀⠀⠈⢳⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠂⠭⠝⣒⠻⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀      
        """
        print(colored((ascii),color = "magenta"))
        folder_path = input("Enter the folder: ")
        self.read_songs_from_folder(folder_path)
        print(colored("File Initialized", color="magenta"))
        while True:
            print(colored("""\nOptions: [l]ist songs, [p]lay, [pause/resume], [s]top, [n]ext, [b]ack
shuffle, [f]orward, [r]everse, [q]uit""", color="magenta"))
            choice = input(colored("Choose an option: ", color="magenta")).lower()
            if choice == 'l':
                self.list_songs()
            elif choice == 'p' or choice == 'play':
                song_index = input("Enter song number to play: ")
                self.play_song(song_index)
            elif choice == 's' or choice == 'stop':
                self.stop_song()
            elif choice == 'n' or choice == 'next':
                self.next_song()
            elif choice == 'b' or choice == 'back':
                self.previous_song()
            elif choice == 'f' or choice == 'forward':
                seconds = int(input("Enter the number of seconds to skip forward: "))
                self.seek_song(seconds)
            elif choice == 'r' or choice == 'reverse':
                seconds = int(input("Enter the number of seconds to skip backward: "))
                self.seek_song(-seconds)
            elif choice == 'shuffle':
                self.shuffle_songs()
            elif choice == 'q' or choice == 'quit':
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    music_player = MusicPlayer()
    music_player.run()