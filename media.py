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

class PDFMedia:
    def __init__(self, src, resources):
        self.src = src
        self.resources = resources

    def getObject(self):
        link = "{}/{}".format(self.resources, self.src) if self.resources else self.src
        return "<a href={}><strong>PDF file</strong></a>".format(link)

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
        src = src[1:] # WhatsApp puts an invisible unicode character (\u200e) just before the name of a media file

        pattern = re.compile(".*\.(jpg|opus|mp3|mp4|vcf|pdf|loc)")
        match = pattern.match(src)

        if match is None:
            raise LookupError("Unknown filetype: " + src)

        if 'loc' not in src:
            if not path.isfile(self.resources + "/" + src):
                raise IOError()

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
            return PDFMedia(src, self.resources)
        elif filetype == "loc":
            return LocationMedia(src, self.resources)
