import winsound

def play_sound(file_path):
    winsound.PlaySound(file_path, winsound.SND_FILENAME)

# Provide the path to the sound file
sound_file_path = "C:\\Users\\PC\\OneDrive\\Desktop\\LaoODetection_person_detection\\LaoODetection\\sounds\\hello1.wav"

# Play the sound
play_sound(sound_file_path)


