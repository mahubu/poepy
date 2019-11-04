from random import choice

from bs4 import BeautifulSoup
from p5 import fill, text_align, text, random_uniform, text_font, text_width
from requests import get

from font import DEFAULT_FONT_SIZE, get_fonts

DEFAULT_SENTENCE_URL = 'https://www.eternels-eclairs.fr/haikus-japonais.php'


class Sentence:
    """
    This class defines a sentence composed of any number of letters.
    """

    def __init__(self, letters, ready=False):
        """
        Constructor
        :param letters: the letters composing the sentence.
        :param ready: whether or not the sentence is ready to be written & read.
        """
        self.letters = letters
        self.ready = ready

    def regrouped(self):
        """
        Regroup the letters composing the sentence.
        """
        for letter in self.letters:
            if not letter.regrouped():
                return False
        return True

    def __str__(self):
        return ''.join(map(str, self.letters))


class Letter:
    """
    This class defines a letter destined to be written & read.
    """

    def __init__(self, x, y, char, font):
        """
        Constructor
        :param x: the X coordinate of the letter on the window.
        :param y: the T coordinate of the letter on the window.
        :param char: the character defining the letter.
        :param font: the font used to write the letter.
        """
        self.character = char
        self.font = font
        self.home_x = x
        self.home_y = y
        self.x = x
        self.y = y

    def display(self):
        """
        Display the letter on the window.
        """
        fill(0)
        text_align("LEFT")
        text_font(self.font)
        text(self.character, (self.x, self.y))

    def disperse(self):
        """
        Move the letter randomly on the window.
        """
        self.x += random_uniform(-2, 2)
        self.y += random_uniform(-2, 2)

    def regroup(self):
        """
        Bring the letter on the screen nearer from its original position.
        """
        self.x += (self.home_x - self.x) / 4
        self.y += (self.home_y - self.y) / 4

    def regrouped(self):
        """
        Whether or not the letter is close enough from its original position.
        :return: True or False
        """
        return abs(self.x - self.home_x) < 0.1 and abs(self.y - self.home_y) < 0.1

    def __str__(self):
        return self.character


def get_corresponding_letter(index, sentence):
    """
    Get the letter corresponding to the index in the given sentence
    :param index: the wanted index.
    :param sentence: the reference sentence.
    :return: the corresponding letter if found, 'None' otherwise.
    """
    if index < len(sentence.letters):
        return sentence.letters[index]
    else:
        return None


def enumerate_sentence(sentence):
    """
    Enumerate a sentence through its letters and theirs positions on the screen.
    :param sentence: the sentence to enumerate.
    :return: a tuple composed of a position on the screen and a letter.
    """
    x = 0
    for letter in sentence:
        yield (x, letter)
        x += text_width(letter.character)


def create_sentence(characters, fonts):
    """
    Create a sentence.
    :param characters: the characters composing the sentence.
    :param fonts: the fonst used to write the sentence.
    :return: the sentence.
    """
    # TODO initialization with DEFAULT_FONT_SIZE ?
    position_x = DEFAULT_FONT_SIZE
    letters = []
    for character in characters:
        font = choice(fonts)
        letters.append(Letter(position_x, DEFAULT_FONT_SIZE, character, font))
        text_font(font)
        position_x += text_width(character)
    return Sentence(letters)


def get_sentences(sentence_fonts, sentence_url=DEFAULT_SENTENCE_URL):
    """
    Retrieve the sentence from the given URL with the given fonts.
    :param sentence_fonts: the fonts used for writing the sentences.
    :param sentence_url: the URL where the sentences can be retrieved from.
    :return: the sentences.
    """
    response = get(sentence_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    sentences = []
    for element in soup.find_all('p', class_='poeme_texte'):
        t = element.get_text()
        for line in t.splitlines():
            # TODO replace needed ?
            verse = line.replace('\t', '')
            if verse.strip():
                sentences.append(create_sentence(verse, sentence_fonts))

    return sentences


if __name__ == '__main__':
    f = get_fonts()
    s = get_sentences(f)
    print(', '.join(map(str, s)))
