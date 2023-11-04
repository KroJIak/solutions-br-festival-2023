import os

images = os.listdir('grtghrth/images')
txts = os.listdir('ehgdfgbdf/obj_train_data')

for file in images:
    name = file[:file.rfind('.')]
    filetxt = f'{name}.txt'
    if filetxt not in txts:
        os.remove(f'grtghrth/images/{file}')