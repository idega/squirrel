# Installation

## CentOS

### mod_wsgi
1. To run `squirrel` you will need to add python support to your apache http server. Execute the following command:

		sudo yum install mod_wsgi

### python-imaging (PIL)
1. Squirrel uses `python-imaging` for generating image thumbnails. Install `python-imaging` with the following command:

		sudo yum install python-imaging

### httpd
1. Make sure `mod_wsgi` is loaded.

2. Edit `/etc/httpd/conf/httpd.conf` and set `wsgi` socket prefix. Otherwise you will get permission denied exception when running `wsgi` in daemon mode.

		WSGISocketPrefix /var/run/wsgi

2. Edit `/etc/httpd/conf.d/virtualhosts.conf` and add virtual host configuration for squirrel:

		<VirtualHost media.test.xperious.com:80>
			ServerName media.test.xperious.com
			DocumentRoot /var/squirrel/xperious
			ErrorLog /var/log/httpd/xperiousmedia_error_log
			CustomLog /var/log/httpd/xperiousmedia_log combined
			WSGIDaemonProcess media.test.xperious.com processes=1 threads=200 display-name=%{GROUP}
			WSGIProcessGroup media.test.xperious.com
			WSGIScriptAliasMatch ^/content/(.*) /var/squirrel/xperious/squirrel.py
			SetEnv REMOTE_USER user
			SetEnv REMOTE_PASS pass
			SetEnv REMOTE_ROOT http://core.test.xperious.com
			ExpiresActive On
    		ExpiresDefault "access plus 1 day"
			<Directory /var/squirrel/xperious>
	    	Order allow,deny
				Allow from all
			</Directory>
		</VirtualHost>

### /etc/hosts
1. Make sure your system is aware of virtual host. Edit `/etc/hosts`:

		10.1.1.186      media.test.xperious.com


## MAC OS X
Just in case if you want to deploy it to your local machine.

### mod_wsgi
1. Do some magic for brew on mountain lion.

		sudo ln -s /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain /Applications/Xcode.app/Contents/Developer/Toolchains/OSX10.8.xctoolchain
		
2. Before proceeding make sure `brew doctor` is ok

3. Add brew apache formulas.

		brew tap homebrew/apache

4. Install mod_wsgi.

		brew install mod_wsgi
		
### python-imaging (PIL)
1. Make sure `brew doctor` is ok
2. Install `brew` python:

		brew install python

3. Add `brew` python formulas:

		brew tap samueljohn/python

4. Install PIL fork called `Pillow` (makes life so much easier):

		brew install pillow

### httpd
1. Follow CentOS guide. The only difference is `mod_wsgi.so` location on Mac OS X.

        LoadModule wsgi_module /usr/local/Cellar/mod_wsgi/3.4/libexec/mod_wsgi.so

2. Just a reminder. Native httpd daemon logs on Mac OS X are under `/private/var/log/apache2/`. To restart httpd use `sudo apachectl restart`.