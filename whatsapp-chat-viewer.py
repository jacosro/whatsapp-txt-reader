#!/usr/bin/python3

import sys
import re
import os
import argparse
import subprocess
from parsing import Parser
from messages import Datestamp, Bubble

css_file = os.path.abspath(os.path.dirname(__file__)) + '/assets/style.css'


def start(file, resources):

    content = ""

    with open(file, 'r') as f:
        content = f.readlines()

    search = re.compile("\d+/\d+/\d+ \d+:\d+ - ([^:]+): (.+)")

    names = []

    for line in content:
        match = search.match(line)
        if match:
            name = match.group(1)
            message = match.group(2)
            if message is not None:
                match = re.compile("^https://maps.google.com/").match(message)
                if match is None:
                    if name not in names and len(name) <= 25:  # Whatsapp's name limit is 25 characters
                        names.append(name)

    print("Which one are you?\n\t{}".format(
        '\n\t'.join(
            ['{}. {}'.format(num + 1, name) for num, name in enumerate(names)]
        )))

    me = names[0]

    while True:
        _input = input('Type one of the above numbers: ')
        try:
            selected = int(_input) - 1
            me = names[selected]
            break
        except:
            continue

    parser = Parser(names, me)

    body = []

    current_date = ""
    for date, bubble in parser.parse(content, resources):
        if date is None:  # Means that the last message contained a linebreak
            formerBubble = body[-1]
            if isinstance(formerBubble, Bubble):
                formerBubble.setMessage(formerBubble.message + bubble)  # In this case, data received is (None, string)
        else:
            if date != current_date:
                body.append(Datestamp(date))
                current_date = date

            formerBubble = body[-1]
            if isinstance(formerBubble, Bubble) and isinstance(bubble, Bubble):
                if formerBubble.name == bubble.name:
                    bubble.doHideName()
                    formerBubble.doHideArrow()
                else:
                    formerBubble.addSeparation()

            body.append(bubble)

    HTML = """<!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Chat With {}</title>
      <link rel="stylesheet" type="text/css" href="{}">
    </head>
    <body>

    <div class="speech-wrapper">
    {}
    </div>

    </body>
    </html>""".format(me, css_file, ''.join([message.inflate() for message in body]))

    filename = file.replace(' ', '_').replace('.txt', '.html')

    with open(filename, 'w') as f:
        f.write(HTML)

    err = open(os.devnull, 'w')  # Redirect to nowhere
    subprocess.call(["python", "-m", "webbrowser", "-t", filename], stdout=err, stderr=err)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The WhatsApp text file")
    parser.add_argument("resources_dir", default='.', nargs='?', help="The directory of media files. If not set, it will try to search in current directory")
    args = parser.parse_args()

    if not args.file.endswith(".txt"):
        print("The file must be a WhatsApp conversation text file (.txt)")
        sys.exit(1)

    try:
        start(args.file, args.resources_dir)
    except KeyboardInterrupt:
        print()
