# This was originally written to proxy and cache images
# from JCR repository. Cache directory can be cleaned
# when required. Image cache will be restored on first
# request. This also can generate image thumbnails when
# required. Just use width parameter in the request for
# image: '.../product/example.png?w=100'.


import os
import urllib2
import base64
from cgi import parse_qs
from cStringIO import StringIO
from PIL import Image


def application(environ, start_response):

      uri = environ['REQUEST_URI']

      width = int(parse_qs(environ['QUERY_STRING']).get('w', [800])[0])

      file_name = urllib2.unquote(os.path.basename(uri).split("?")[0])
      file_path = urllib2.unquote('/cache' + os.path.split(uri)[0]) + "/" + str(width)
      file      = file_path + '/' + file_name
               
      working_dir = os.path.split(environ['SCRIPT_FILENAME'])[0]
      local_dir   = working_dir + file_path
      local_file  = local_dir + '/' + file_name
      remote_uri  = environ['REMOTE_ROOT'] + uri.split("?")[0]

      # Do not process gifs because they cause too much trouble
      if file_name.endswith('gif'):
          start_response('301 Redirect', [('Location', remote_uri)])
          return []

      if not os.path.exists(local_file):
          request = urllib2.Request(remote_uri)
          
          # Check whether username was set and use BASIC auth if required
          if (environ['REMOTE_USER']):
              base64string = base64 \
                  .encodestring('%s:%s' % (environ['REMOTE_USER'], environ['REMOTE_PASS'])) \
                  .replace('\n', '')
              request.add_header("Authorization", "Basic %s" % base64string)


          # Download image from the source and save it locally
          image = Image.open(StringIO(urllib2.urlopen(request).read()))
          image.thumbnail((width, width), Image.ANTIALIAS)
          if not os.path.exists(local_dir):
              os.makedirs(local_dir)
          image.save(local_file, "JPEG", quality = 80)


      # Returning HTTP 200 with Location causes internal
      # HTTP server redirect (invisible to the browser)
      start_response('200 OK', [('Location', file)])


      return []
