import string
import random
import secrets
import re
from pathlib import Path

SPECIAL_CHARS = list('!@#$%^&*(),.')

VOWELS = list('aeiou')
CONSONANTS = list(''.join(set(string.ascii_lowercase) - set('aeiou')))

class password_generator(object):

    def __init__(self, num_passwords=10, length_password=14, case_probability=0.05, digits_prob=0.1, special_salt_prob=0.1):
        if digits_prob + special_salt_prob > 1.:
            raise ValueError('Probability of digit and special character salting too high.')
        self.num_passwords = num_passwords
        self.length_password = length_password
        self.case_probability = case_probability
        self.digits_prob = digits_prob
        self.special_salt_prob = special_salt_prob
        self.password = ''

    def build_basic_phonetic(self):
        while self.length_password > 0:
            rand_draw = random.random()
            rand_chars = ''
            if rand_draw > (1 - self.special_salt_prob):
                # special character
                rand_chars = secrets.choice(SPECIAL_CHARS)
            else:
                if rand_draw > (1 - self.special_salt_prob - self.digits_prob):
                    # random digit
                    rand_chars = secrets.choice(string.digits)
                else:
                    if rand_draw < (1 - self.special_salt_prob - self.digits_prob) / 2:
                        # cvv
                        for i in 'cvv':
                            if i == 'c':
                                rand_chars += secrets.choice(CONSONANTS)
                            else:
                                rand_chars += secrets.choice(VOWELS)
                        rand_chars = ''.join([c.upper() if (random.random() > (1 - self.case_probability)) else c for c in rand_chars])
                    else:
                        # cv
                        for i in 'cv':
                            if i == 'c':
                                rand_chars += secrets.choice(CONSONANTS)
                            else:
                                rand_chars += secrets.choice(VOWELS)
                        rand_chars = ''.join([c.upper() if (random.random() > (1 - self.case_probability)) else c for c in rand_chars])
                
            self.length_password -= len(rand_chars)
            self.password += rand_chars
            # print(self.password)
        if self.length_password < 0:
            self.password = self.password[:self.length_password]

    def basic_phonetic(self):
        pass_length = self.length_password
        passwords = []
        for k in range(self.num_passwords):
            self.length_password = pass_length
            self.build_basic_phonetic()
            passwords.append(self.password)
            print(len(self.password))
            self.password = ''

        print(passwords)


    def generate_markov_chain(self, examples=100, text_files=r'text_corpus'):
        def build_pairs(text):
            for i in range(len(text) - 1):
                yield (text[i], text[i+1])

        def build_dict(text):
            markov = {}
            for char1, char2 in build_pairs(text):
                if char1 in markov.keys():
                    markov[char1].append(char2)
                else:
                    markov[char1] = [char2]
            return markov

        def make_text(text_files, example_num):
            fpath = Path(text_files)
            if not fpath.exists():
                raise ImportError('Point to a location where text files exist')
            text_files = list(fpath.rglob('*.txt'))
            random.shuffle(text_files)
            full_text = []
            for file_now in text_files:
                example_num -= 1
                if example_num <= 0:
                    break
                with open(str(file_now)) as fid:
                    text_now = fid.read()
                    text_now = text_now.lower()
                    rgx = re.compile('[%s]' % '\\\' \"-'.join(SPECIAL_CHARS))
                    squashed_text = rgx.sub('', text_now)
                    full_text.append(squashed_text)
            return ''.join(full_text)

        full_text = make_text(text_files, examples)
        markov_dict = build_dict(full_text)
        build_chain = [secrets.choice(full_text)]
        for i in range(self.length_password):
            build_chain.append(secrets.choice(markov_dict[build_chain[-1]]))
        full_chain = ''.join(build_chain)
        # keep repeat letters below 3
        repeats = re.findall(r'((\w)\2{2,})', full_chain)
        for rep_now in repeats:
            idx = full_chain.find(rep_now[0])
            for j in range(len(rep_now[0]) - 2):
                full_chain = full_chain[:idx+2+j] + secrets.choice(full_text) + full_chain[idx+3+j:]
        return full_chain

    def markov_chain(self):
        passwords = []
        for k in range(self.num_passwords):
            passwords.append(self.generate_markov_chain())
        print(passwords)
