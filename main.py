from time import process_time

from p5 import size, background, run

from font import DEFAULT_FONT_SIZE, get_fonts
from sentence import get_sentences, get_corresponding_letter, enumerate_sentence
from speech import say

fonts = get_fonts()
sentences = get_sentences(fonts)

start_time = process_time()
from_sentence = None
to_sentence = None

window_size_x = 0
for s in sentences:
    if len(s.letters) > window_size_x:
        window_size_x = len(s.letters)
window_size_x = window_size_x * DEFAULT_FONT_SIZE / 2
window_size_y = DEFAULT_FONT_SIZE * 3


def setup():
    """
    Set up the displaying window.
    """
    size(window_size_x, window_size_y)


def draw():
    """
    Write & read the sentences.
    """
    global start_time, from_sentence, to_sentence
    background(255)

    if from_sentence is None:
        from_sentence = sentences.pop(0)

    if to_sentence is None:
        to_sentence = sentences.pop(0)
        start_time = process_time()

    elapsed_time = process_time() - start_time
    if elapsed_time < 10:
        for letter in from_sentence.letters:
            letter.display()
            letter.disperse()
        if not from_sentence.ready:
            from_sentence.ready = True
            say(from_sentence)
    else:
        if not to_sentence.ready:
            to_sentence.ready = True
            for index, to_letter in enumerate(to_sentence.letters):
                from_letter = get_corresponding_letter(index, from_sentence)
                if from_letter is not None:
                    from_letter.display()
                    to_letter.x = from_letter.x
                    to_letter.y = from_letter.y
                    to_letter.home_x = from_letter.home_x
                    to_letter.home_y = from_letter.home_y
                to_letter.display()
        else:
            if not to_sentence.regrouped():
                for letter in to_sentence.letters:
                    letter.display()
                    letter.regroup()
            else:
                for width, letter in enumerate_sentence(to_sentence.letters):
                    letter.display()
                    # TODO add DEFAULT_FONT_SIZE ?
                    letter.x = width + DEFAULT_FONT_SIZE
                    letter.home_x = width + DEFAULT_FONT_SIZE
                say(to_sentence)
                from_sentence = to_sentence
                to_sentence = None


if __name__ == '__main__':
    run()
