from os import listdir, mkdir, walk, close
from os.path import isfile, exists, join
from shutil import copy, rmtree
from tempfile import mkdtemp, mkstemp
from zipfile import ZipFile

from bs4 import BeautifulSoup
from p5 import create_font
from requests import get

DEFAULT_FONT_SIZE = 64
DEFAULT_FONT_DIRECTORY = 'fonts'
DEFAULT_FONT_EXTENSION = ('.otf', '.ttf')
DEFAULT_FONT_URL = 'http://www.misprintedtype.com/fonts/freeware/'


def get_fonts(font_directory=DEFAULT_FONT_DIRECTORY, font_url=DEFAULT_FONT_URL):
    if not exists(font_directory):
        mkdir(font_directory)

    # Retrieve the available fonts from the given directory, if possible.
    fonts = [create_font(join(font_directory, font.lower()), DEFAULT_FONT_SIZE) for font in listdir(font_directory) if
             font.lower().endswith(DEFAULT_FONT_EXTENSION) and isfile(join(font_directory, font))]

    # Get fonts from the given website and install then into the given directory.
    if not fonts:
        temp_directory = mkdtemp()
        temp_file = mkstemp('.zip', None, temp_directory)

        response = get(font_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for el in soup.find_all('a', class_='download'):
            link = el['href']
            response = get(font_url + "../.." + link)
            with open(temp_file[1], 'wb') as file:
                file.write(response.content)
            with ZipFile(temp_file[1], 'r') as zip_file:
                zip_file.extractall(temp_directory)

        close(temp_file[0])

        for (root, dirs, files) in walk(temp_directory):
            for file in files:
                if not file.lower().startswith('.') and file.lower().endswith(DEFAULT_FONT_EXTENSION):
                    copy(join(root, file), font_directory)
                    fonts.append(create_font(join(font_directory, file.lower()), DEFAULT_FONT_SIZE))

        rmtree(temp_directory)

    return fonts


if __name__ == '__main__':
    get_fonts()
