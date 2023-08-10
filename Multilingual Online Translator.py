import sys
import requests
import argparse
import ExceptionClasses as ex
from bs4 import BeautifulSoup

lan_support = ["arabic", "german", "english", "spanish", "french", "hebrew",
               "japanese", "dutch", "polish", "portuguese", "romanian",
               "russian", "turkish"]


def request_web_page(lan_o: str, lan_t: str, word: str):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://context.reverso.net/translation/{0}-{1}/{2}".format(lan_o.lower(), lan_t.lower(), word)

    while url != "":
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r
        elif r.status_code == 404:
            raise ex.WordNotFound(word)
        else:
            raise ex.InternetException


def scrap_terms(r: requests.models.Response):
    soup = BeautifulSoup(r.content, 'html.parser')
    terms = soup.find_all(class_="display-term")
    l_words = []
    for term in terms:
        l_words.append(term.text)
    raw_ex = soup.find_all(class_="text")
    examples = []
    for example in raw_ex:
        if example.find('em'):
            raw_string = example.text
            cleaned_text = raw_string.replace("  ", "").replace("\n", "").replace("\r", "")
            examples.append(cleaned_text)

    return l_words, examples


def Gen_Report(word: str, l_words: list, examples: list, format_lan: str):
    file = open(word + ".txt", mode="w", encoding="utf-8")
    print("\n{0} Translations:".format(format_lan))
    file.write("{0} Translations:\n".format(format_lan))
    for count, word in enumerate(l_words):
        if count < 5:
            print(word)
            file.write(word + "\n")
        else:
            file.write("\n")
            break

    print("\n{0} Examples:".format(format_lan))
    file.write("{0} Examples:\n".format(format_lan))
    for count, example in enumerate(examples):
        if count < 10:
            if count % 2 != 0:
                print(example + "\n")
                file.write(example + "\n")
                file.write("\n")
            else:
                print(example)
                file.write(example + "\n")
        else:
            break
    file.close()


def option_zero(lan_O: int, word: str):
    list_lan_zero = lan_support
    origin = list_lan_zero.pop(lan_O)
    file = open(word + ".txt", mode="w", encoding="utf-8")
    for lan in list_lan_zero:
        try:
            r = request_web_page(origin, lan, word)
        except ex.InternetException as e:
            print(e)
            sys.exit(1)
        except ex.WordNotFound as e:
            print(e)
            sys.exit(1)
        l_words, examples = scrap_terms(r)
        file.write("{0} Translations:\n".format(lan))
        print("{0} Translations:".format(lan))
        file.write(l_words[0] + "\n")
        print(l_words[0] + "\n")

        file.write("\n")
        file.write("{0} Example:\n".format(lan))
        print("{0} Example:".format(lan))

        file.write(examples[0] + "\n")
        file.write(examples[1] + "\n")
        print(examples[0])
        print(examples[1] + "\n")
        file.write("\n")
    file.close()


def error_managment(source, target, word):
    error_rise = False
    if source not in lan_support:
        error_rise = True
        raise ex.NotSupportedLan(source)
    if target not in lan_support and target != "all":
        error_rise = True
        raise ex.NotSupportedLan(target)
    if not request_web_page(source, target, word):
        error_rise = True
        raise ex.WordNotFound(word)

    return error_rise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This program translate an word from one language to another")
    
    parser.add_argument("source", help="You need to choose a language from the ones "
                                       "supported")
    parser.add_argument("target", help="You need to choose a language "
                                       "from the ones supported or "
                                       "'all' of them")
    parser.add_argument("word", help="Write a word in the source language to translate")

    args = parser.parse_args()

    try:
        error_managment(args.source, args.target, args.word)
    except Exception as e:
        print(e)
        sys.exit(1)

    if args.target == "all":
        option_zero(lan_support.index(args.source), args.word)
    else:
        try:
            r = request_web_page(args.source, args.target, args.word)
        except ex.InternetException as e:
            print(e)
            sys.exit(1)
        except ex.WordNotFound as e:
            print(e)
            sys.exit(1)
        l_words, examples = scrap_terms(r)
        Gen_Report(args.word, l_words, examples, args.target)