from pafy import new

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

# video = new('https://www.youtube.com/watch?v=_XkgYJKaSS0',ydl_opts=ytdl_format_options)
# print(video.getbestaudio().download())

#['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_active', '_bitrate', '_dimensions', '_extension', '_filename', '_fsize', '_info', '_itag', '_mediatype', '_notes', '_parent', '_quality', '_rawbitrate', '_rawurl', '_resolution', '_threed', '_url',
# 'bitrate', 'cancel', 'dimensions', 'download', 'encrypted', 'extension', 'filename', 'generate_filename', 'get_filesize', 'itag', 'mediatype', 'notes', 'quality', 'rawbitrate', 'resolution', 'threed', 'title', 'url', 'url_https']
