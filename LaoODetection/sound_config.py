import winsound

auidio_file_1 = r"LaoODetection/sounds/hell0_CE_president.wav"
auidio_file_2 = r"LaoODetection/sounds/hello_CE.wav"
auidio_file_3 = r"LaoODetection/sounds/hello_ceit.wav"
auidio_file_4 = r"LaoODetection/sounds/president_iceit.wav"


def play_sound():
    sound_file_path = auidio_file_1
    winsound.PlaySound(sound_file_path, winsound.SND_FILENAME)




