#coding=utf8
import re
import vcf
from os import path

class ImageMedia:

    def __init__(self, src, resources):
        self.src = src
        self.resources = resources

    def getObject(self):
        link = "{}/{}".format(self.resources, self.src) if self.resources else self.src
        return '<img src="{}" style="width:304px;height:228px;"></img>'.format(link)

class VoiceNoteMedia:
    def __init__(self, src, resources):
        self.src = src
        self.resources = resources

    def getObject(self):
        link = "{}/{}".format(self.resources, self.src) if self.resources else self.src
        return '''
    <strong>Voice Note: </strong><audio controls>
      <source src="{}" type="audio/ogg">
    </audio>
    '''.format(link)

class AudioMedia:
    def __init__(self, src, resources):
        self.src = src
        self.resources = resources

    def getObject(self):
        link = "{}/{}".format(self.resources, self.src) if self.resources else self.src
        return '''
    <strong>Audio: </strong><audio controls>
      <source src="{}" type="audio/mpeg">
    </audio>
    '''.format(link)

class VideoMedia:
    def __init__(self, src, resources):
        self.src = src
        self.resources = resources

    def getObject(self):
        link = "{}/{}".format(self.resources, self.src) if self.resources else self.src
        return '''
        <video width="320" height="240" controls>
          <source src="{}" type="video/mp4">
        </video>
        '''.format(link)

class ContactMedia:
    def __init__(self, src, resources):
        self.src = src
        self.resources = resources

    def getObject(self):
        parser = vcf.VCFParser("{}".format("{}/{}".format(self.resources, self.src) if self.resources else self.src))
        number = parser.getNumber()
        return '''
        <strong>Contact: </strong>{}: {}
        '''.format(self.src[:len(self.src) - 4], number)

class DocumentMedia:
    def __init__(self, src, resources):
        self.src = src
        self.resources = resources

    def getObject(self):
        link = "{}/{}".format(self.resources, self.src) if self.resources else self.src
        return "<a href={}><strong>Document</strong></a>".format(link)

class LocationMedia:
    def __init__(self, src, resources):
        self.src = src
        self.resources = resources

    def getObject(self):
        link = self.src[:len(self.src) - 4]
        return "<a href={}><strong>Location</strong></a>".format(link)


class Media():

    def __init__(self, rsrcs):
        self.resources = rsrcs

    def getMedia(self, src):
        if not src.endswith('loc'):
            src = src[1:]  # WhatsApp puts an invisible unicode character (\u200e) just before the name of a media file
            if not path.isfile(self.resources + "/" + src):
                raise IOError()

        pattern = re.compile(".*\.(jpg|opus|mp3|mp4|vcf|pdf|loc)")
        match = pattern.match(src)

        if match is None:
            raise LookupError("Unknown filetype: " + src)

        filetype = match.group(1)

        if filetype == "jpg":
            return ImageMedia(src, self.resources)
        elif filetype == "opus":
            return VoiceNoteMedia(src, self.resources)
        elif filetype == "mp3":
            return AudioMedia(src, self.resources)
        elif filetype == "mp4":
            return VideoMedia(src, self.resources)
        elif filetype == "vcf":
            return ContactMedia(src, self.resources)
        elif filetype == "pdf":
            return DocumentMedia(src, self.resources)
        elif filetype == "loc":
            return LocationMedia(src, self.resources)


def parse_media(resources_dir, msg):
    media_pattern = re.compile("[A-Z]{3}-[0-9]{8}-WA[0-9]{4}\.[^\s]+")
    location_pattern = re.compile("^https://maps.google.com/[^\s]+")
    contact_pattern = re.compile("^[^.]+\.vcf$")

    res = None

    if location_pattern.match(msg):
        res = LocationMedia
    elif contact_pattern.match(msg):
        res = ContactMedia
    elif media_pattern.match(msg):
        if msg.startswith('IMG'):
            res = ImageMedia
        elif msg.startswith('VID'):
            res = VideoMedia
        elif msg.startswith('PTT'):
            res = VoiceNoteMedia
        elif msg.startswith('AUD'):
            res = AudioMedia
        else:
            res = DocumentMedia

    if res is None:
        raise ValueError("Unrecognized media: {}".format(msg))

    return res(msg, resources_dir)
