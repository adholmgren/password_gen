import string
import random
import secrets

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
