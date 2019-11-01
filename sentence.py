from random import choice

from bs4 import BeautifulSoup
from p5 import fill, text_align, text, random_uniform, text_font, text_width
from requests import get

from font import DEFAULT_FONT_SIZE, get_fonts

DEFAULT_SENTENCE_URL = 'https://www.eternels-eclairs.fr/haikus-japonais.php'


class Sentence:
    def __init__(self, letters, ready=False):
        self.letters = letters
        self.ready = ready

    def regrouped(self):
        for letter in self.letters:
            if not letter.regrouped():
                return False
        return True

    def __str__(self):
        return ''.join(map(str, self.letters))


class Letter:
    def __init__(self, x, y, char, font):
        self.character = char
        self.font = font
        self.home_x = x
        self.home_y = y
        self.x = x
        self.y = y

    def display(self):
        fill(0)
        text_align("LEFT")
        text_font(self.font)
        text(self.character, (self.x, self.y))

    def disperse(self):
        self.x += random_uniform(-2, 2)
        self.y += random_uniform(-2, 2)

    def regroup(self):
        self.x += (self.home_x - self.x) / 4
        self.y += (self.home_y - self.y) / 4

    def regrouped(self):
        return abs(self.x - self.home_x) < 0.1 and abs(self.y - self.home_y) < 0.1

    def __str__(self):
        return self.character


def get_corresponding_letter(index, sentence):
    if index < len(sentence.letters):
        return sentence.letters[index]
    else:
        return None


def enumerate_sentence(sentence):
    x = 0
    for letter in sentence:
        yield (x, letter)
        x += text_width(letter.character)


def create_sentence(sentence, fonts):
    # TODO initialization with DEFAULT_FONT_SIZE ?
    position_x = DEFAULT_FONT_SIZE
    letters = []
    for character in sentence:
        font = choice(fonts)
        letters.append(Letter(position_x, DEFAULT_FONT_SIZE, character, font))
        text_font(font)
        position_x += text_width(character)
    return Sentence(letters)


def get_sentences(sentence_fonts, sentence_url=DEFAULT_SENTENCE_URL):
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
