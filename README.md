# OpenHost

### What is this?
Host your html5 site on docker for free with OpenHost! You also get a simple modern dashboard where you can setup your site and see the system info. 
This is all for free, just fire up a docker container with OpenHost running on it!

### How to setup the container

1. Run ```docker pull jessiflessi/openhost``` in the terminal
2. Run ```docker run -d -p 4545:4545 jessiflessi/openhost``` in the terminal
3. Your done

# How to use?
1. If you first start the container go to [yourip]:4545/login (replace [yourip] with the actual ip)
2. Set your username and password
3. Login with the username and password you just made
4. In the admin dashboard upload your html css and js files
5. To go to the site go to [yourip]:4545 (replace [yourip] with the actual ip)
6. if your file is not a index.html but for example cool.html you need to go to [yourip]:4545/cool.html replace cool with your file name

# 

Current Version: ```1.0```
