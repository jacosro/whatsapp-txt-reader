#!/usr/bin/python3
import re
from media import Media
from messages import Bubble, Broadcast


class Parser:

    def __init__(self, names, me):
        self.names = names
        self.me = me

        #self.timeregex = re.compile("^(\d+/\d+/\d+), (\d+:\d+) - .*")
        self.regex = re.compile("^(\d+/\d+/\d+) (\d+:\d+) - (({}): )?(.*)".format('|'.join(names)))
        self.retext = re.compile("(.*\.(jpg|opus|mp3|mp4|vcf|pdf)) \([a-z]+ [a-z]+\)$")  # IMG-20170327-WA00021.jpg (file attached)
        self.locationregex = re.compile("(.*): (http(s)?://maps.google.com/.*)$")

    def parse(self, content, resources):
        media = Media(resources)

        for line in content:
            match = self.regex.match(line)
            if match is not None:

                date = match.group(1)
                time = match.group(2)
                name = match.group(4)
                message = match.group(5)

                if name:
                    mediamatch = self.retext.match(message)

                    if mediamatch:
                        try:
                            src = mediamatch.group(1)
                            message = media.getMedia(src).getObject()
                        except IOError:
                            message = "<strong>Could not find file: </strong>{}".format(src)
                    else:
                        locationmatch = self.locationregex.match(message)

                        if locationmatch:
                            message = media.getMedia(locationmatch.group(2) + ".loc").getObject()

                    yield (date, Bubble(name, message, time, name != self.me))

                else:
                    # Broadcast message
                    yield (date, Broadcast(message))
            else:
                # It's an image with a message
                yield (None, line)
