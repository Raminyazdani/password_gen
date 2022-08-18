import argparse
import itertools
import random
import string
import logging

test_random_seed = random.random()
length_random=len(str(test_random_seed)[2:])
test_random_seed = test_random_seed*(10**length_random)
random.seed(test_random_seed)

logger = logging.getLogger("password_logger")
log_format = logging.Formatter("%(asctime)s-(%(name)-10s) -%(levelname)-16s -%(message)s")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("password.log", "a", encoding="utf-8")
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)


class ArgumentTypeErrorRange(Exception):

    def __init__(self, range, logger):
        logger.log(logging.CRITICAL,
                   f"password cannot created : because of invalid wrong value range min: {range[0]} : max: {range[1]} ")
        super().__init__(f"wrong value range min: {range[0]} : max: {range[1]} ")


class ArgumentTypeErrorPasswords(Exception):

    def __init__(self, words, logger):
        logger.log(logging.CRITICAL,
                   f"password cannot created : because of wrong value for words only password hashable characters in {words} ")

        super().__init__(f"wrong value for words only password hashable characters in {words} ")


class ArgumentTypeErrorStartWords(Exception):

    def __init__(self, length, logger):
        logger.log(logging.CRITICAL,
                   f"password cannot created : because of wrong value for words . length of initial words are equal to max lenght of password. length:{length}")

        super().__init__(
            f"wrong value for words . length of initial words are equal to max lenght of password. length:{length}")


class ArgumentTypeErrorFreq(Exception):

    def __init__(self, freq, logger):
        logger.log(logging.CRITICAL, f"password cannot created : because of wrong value for products numbers : {freq}")

        super().__init__(f"wrong value for products numbers : {freq}")


# def required_length(nmin, nmax):
#     class RequiredLength(argparse.Action):
#         def __call__(self, parser, args, values, option_string=None):
#             if not nmin <= len(values) <= nmax:
#                 msg = 'argument "{f}" requires between {nmin} and {nmax} arguments'.format(
#                     f=self.dest, nmin=nmin, nmax=nmax)
#                 raise argparse.ArgumentTypeError(msg)
#             setattr(args, self.dest, values)
#
#     return RequiredLength
#
def check_args(args_test):
    test = args_test
    test_list = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    for word in args_test.words:
        if word not in test_list:
            raise ArgumentTypeErrorPasswords(args_test.words, logger)
    for word in args_test.testWords:
        if word not in test_list:
            raise ArgumentTypeErrorPasswords(args_test.testWords, logger)
    if len(args_test.testWords) >= args_test.length[1]:
        raise ArgumentTypeErrorStartWords(args_test.length[1])
    if args_test.L < 0:
        raise ArgumentTypeErrorFreq(args_test.L, logger)
    test.length[0], test.length[1] = test.length[0] - len(args_test.testWords), test.length[1] - len(args_test.testWords)
    if test.length[0]==0:
        test.length[0] +=1
    if args_test.length[0] > args_test.length[1] or test.length[0] > test.length[1]:
        raise ArgumentTypeErrorRange(args_test.Length, logger)
    return test


def make_password(length, freq, words_in, testWords):
    temp_words = words_in
    starting_words = "".join(testWords)
    if temp_words is None:
        temp_length = random.randint(length[0], length[1])
        temp_words = []
        test_list = list(string.ascii_letters + string.digits + "!@#$%^&*()")
        for terms in range(temp_length):
            temp_words.append(random.choice(test_list))
    words = temp_words

    def make_all(words, length):
        for repeat in range(length[0], length[1]):
            list_gen = itertools.permutations("".join(words), repeat)
            for word in list_gen:
                yield starting_words + "".join(word)

    def make_one(words, length):
        temping = words
        temp = ""
        temp_length = random.randint(length[0], length[1])
        for frequency in range(temp_length):
            temp += random.choice(temping)
        return starting_words + temp

    def make_freq(length, freq, words):
        stored = []
        for times in range(freq):
            temp = make_one(words, length)
            if temp not in stored:
                stored.append(temp)
                yield temp

    if freq is False:
        result = make_one(words, length)  #
    elif freq is True:
        result = make_all(words, length)  #
    elif isinstance(freq, int):
        result = make_freq(length, freq, words)
    else:
        result = None
    return result


def print_passwords(result, args):
    count = 1
    tempingstringlog=f"password generator created! words={args.words} output file={args.output.name if args.output != None else args.output} length = [min:{args.length[0]}:max:{args.length[1]}] initial words = {args.testWords}"

    if args.output is None:
        while True:
            try:
                temp = "".join(next(result))
                logger.log(logging.INFO,
                           f"{str(count):8s} password created : {temp} with {tempingstringlog}")
                print(temp)
                count+=1
            except StopIteration:
                break
            except KeyboardInterrupt:
                logger.log(logging.WARNING,
                           f"password creating stop at KeyboardInterrupt")
                print("Interrupted while generating")
            except:
                logger.log(logging.INFO,
                           f"{str(count):8s} password created : {result} with {tempingstringlog}")
                print(result)
                break
    else:
        output = args.output
        while True:
            try:
                temp = "".join(next(result))
                logger.log(logging.INFO,
                           f"{str(count):8s} password created : {temp} with {tempingstringlog}")
                print(temp)
                count+=1
                output.write(temp + "\n")
            except StopIteration:
                break
            except KeyboardInterrupt:
                logger.log(logging.WARNING,
                           f"password creating stop at KeyboardInterrupt")
                print("Interrupted while generating")
            except:
                logger.log(logging.INFO,
                           f"{str(count):8s} password created : {result} with {tempingstringlog}")
                print(result)
                output.write(result + "\n")
                break


parser = argparse.ArgumentParser(description="Python script to generate random passwords", prefix_chars="-+/")
parser.add_argument("-w", "--words", type=str, nargs="+", required=False,
                    help="words include to generate random passwords")
parser.add_argument("-o", "--output", type=argparse.FileType("a"), dest="output", action="store",
                    help="Directs the output file of passwords to a name of your choice", default=None)
parser.add_argument("-l", "--length", type=int, nargs=2, default=[4, 8])
parser.add_argument("-t", "--testWords", type=str, nargs="+", default=[])
group = parser.add_mutually_exclusive_group()
group.add_argument("-L", action="store_false" ,default=False)
group.add_argument("+L", action="store_true")
group.add_argument("/L", type=int, required=False)

args = parser.parse_args()
try:
    temp = check_args(args)
    logger.log(logging.INFO,
               f"password generator created! words={args.words} output file={args.output.name if args.output != None else args.output} length = [min:{args.length[0]}:max:{args.length[1]}] initial words = {args.testWords}")
    result = make_password(temp.length, temp.L, temp.words, temp.testWords)
    print_passwords(result, temp)

except:
    logger.log(logging.ERROR,
               f"cant generate password with :  words={args.words} output file={args.output.name if args.output != None else args.output} length = [min:{args.length[0]}:max:{args.length[1]} initial words = {args.testWords}]")
