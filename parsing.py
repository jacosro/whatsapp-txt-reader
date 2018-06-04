import re
from media import parse_media
from messages import Bubble, Broadcast


class Parser:

    def __init__(self, names, me):
        self.names = names
        self.me = me

        #self.timeregex = re.compile("^(\d+/\d+/\d+), (\d+:\d+) - .*")
        self.regex = re.compile("^(\d+/\d+/\d+) (\d+:\d+) - (({}): )?(.*)".format('|'.join(names)))
        self.mediaregex = re.compile("^.?([A-Z]{3}-[0-9]{8}-WA[0-9]{4}\.[^\s]+) \([a-z]+ [a-z]+\)$")  # IMG-20170327-WA00021.jpg (file attached)
        self.locationregex = re.compile("(.*): (http(s)?://maps.google.com/.*)$")
        self.contactregex = re.compile("(^[^.]+\.vcf) \([a-z]+ [a-z]+\)$")

    def parse(self, content, resources):

        for line in content:
            match = self.regex.match(line)
            if match is not None:

                date = match.group(1)
                time = match.group(2)
                name = match.group(4)
                message = match.group(5)

                if name:
                    mediamatch = self.mediaregex.match(message)
                    locationmatch = self.locationregex.match(message)
                    contactmatch = self.contactregex.match(message)

                    if mediamatch:
                        try:
                            src = mediamatch.group(1)
                            message = parse_media(resources, src).getObject()
                        except IOError:
                            message = "<strong>File not found: </strong>{}".format(src)
                    elif locationmatch:
                        message = parse_media(resources, locationmatch.group(2)).getObject()

                    elif contactmatch:
                        message = parse_media(resources, contactmatch.group(1)).getObject()

                    yield (date, Bubble(name, message, time, name != self.me))

                else:
                    # Broadcast message
                    yield (date, Broadcast(message))
            else:
                # It's an image with a message
                yield (None, line)
