"""
Author: zxcv@csh/asg7201
Description: CLI-based Music player using Python3, PyGame, Random, OS
PS: Don't mind some of the the crappy code. 
TM: expand the music library and add an option to create playlists.
"""
import os
import pygame
import random
import pyfiglet
from termcolor import colored

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.music_library = {
            #Enter your songs here:
            #Example:
            #'1': r"C:\Users\usr\Downloads\Daft Punk - Alive 1997 Official [Full Album].mp3",
            
        }

        """print("Music Library Loaded:")
        for key, song in self.music_library.items():
            print(key,": ",os.path.basename(song))"""

        self.current_song = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 1.0  # Volume level from 0.0 to 1.0
        pygame.mixer.music.set_volume(self.volume)

    def list_songs(self):
        print(colored("Available Songs:",color = "green"))
        if not self.music_library:
            print(colored("No songs available in the library."),color = "green")
            return
        for key, song in self.music_library.items():
            print(colored(key + ": " +os.path.basename(song),color = "green"))

    def play_song(self, song_key):
        if song_key in self.music_library:
            self.current_song = self.music_library[song_key]
            print(colored("Playing: " + os.path.basename(self.current_song), color="green"))
            try:
                pygame.mixer.music.load(self.current_song)
                pygame.mixer.music.play()
                self.is_playing = True
                self.is_paused = False
            except Exception as e:
                print(colored("Error loading song:", {e},color = "green"))
        else:
            print(colored("Song not found!"),color = "green")

    def pause_song(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            print(colored("Paused: ",os.path.basename(self.current_song),color = "green"))
            self.is_paused = True
        elif self.is_paused:
            pygame.mixer.music.unpause()
            print(colored("Resumed: ", os.path.basename(self.current_song),color = "green"))
            self.is_paused = False
        else:
            print(colored("No song is currently playing.",color = "green"))

    def stop_song(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            print(colored("Stopped: ",os.path.basename(self.current_song),color = "green"))
            self.is_playing = False
            self.is_paused = False
        else:
            print(colored("No song is currently playing."),color = "green")

    def next_song(self):
        if self.current_song:
            current_index = list(self.music_library.keys()).index(next(key for key, value in self.music_library.items() if value == self.current_song))
            next_index = (current_index + 1) % len(self.music_library)
            self.play_song(list(self.music_library.keys())[next_index])
        else:
            print(colored("No song is currently playing."),color = "green")

    def previous_song(self):
        if self.current_song:
            current_index = list(self.music_library.keys()).index(next(key for key, value in self.music_library.items() if value == self.current_song))
            previous_index = (current_index - 1) % len(self.music_library)
            self.play_song(list(self.music_library.keys())[previous_index])
        else:
            print(colored("No song is currently playing."),color = "green")

    def shuffle_songs(self):
        keys = list(self.music_library.keys())
        random.shuffle(keys)
        print(colored("Songs shuffled. Now playing:"),color = "green")
        self.play_song(keys[0])

    def set_volume(self, volume):
        if 0 <= volume <= 1:
            self.volume = volume
            pygame.mixer.music.set_volume(self.volume)
            print(colored("Volume set to ", int(volume * 100),color = "green"))
        else:
            print(colored("Volume must be between 0.0 and 1.0.",color = "green"))

    def seek_song(self, seconds):
        if self.is_playing:
            current_position = pygame.mixer.music.get_pos() / 1000  # Get current position in seconds
            new_position = current_position + seconds

            # Ensure new position is non-negative
            new_position = max(0, new_position)
            print(colored(f"Seeking to {new_position:.1f} seconds.",color = "green"))
            pygame.mixer.music.play(0, new_position)
        else:
            print(colored("No song is currently playing.",color = "green"))

    def run(self):
        try:
            print(colored(pyfiglet.figlet_format("CLIotify"),color = "green"))
            while True:
                print(colored("\nOptions: [l]ist songs, [p]lay, [pause/resume], [s]top, [n]ext, [b]ack, [shuffle], [v]olume, [f]forward, [r]everse, [q]uit",color = "green"))
                choice = input(colored("Choose an option: ",color = "green")).strip().lower()

                if choice == 'l':
                    self.list_songs()
                elif choice == 'p':
                    song_key = input(colored("Enter song number to play: ",color = "green"))
                    self.play_song(song_key)
                elif choice in ['pause', 'resume']:
                    self.pause_song()
                elif choice == 's':
                    self.stop_song()
                elif choice == 'n':
                    self.next_song()
                elif choice == 'b':
                    self.previous_song()
                elif choice == 'shuffle':
                    self.shuffle_songs()
                elif choice == 'v':
                    volume_level = float(input(colored("Enter volume level (0.0 to 1.0): ",color = "green")))
                    self.set_volume(volume_level)
                elif choice == 'f':
                    self.seek_song(10) 
                elif choice == 'r':
                    self.seek_song(-10)
                elif choice == 'q':
                    print(colored("Exiting the music player.",color = "green"))
                    break
                else:
                    print(colored("Invalid option. Please try again.",color = "green"))
        except KeyboardInterrupt:
            print(colored("\nExiting the music player.",color = "green"))
            pygame.mixer.music.stop()
        finally:
            pygame.mixer.quit()  # Ensure pygame quits properly

if __name__ == "__main__":
    player = MusicPlayer()
    player.run()