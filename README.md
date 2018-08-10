# Bodhi - Client-Side Vulnerability Playground
Bodhi is a playground focused on learning the exploitation of client-side web vulnerabilities. The playground has a vulnerable application & a bot program which simulates the real-world victim (that being the USP of the project). An attacker having the  knowledge of the vunerability will send a crafted payload which will be accessed by the victim. The attacker needs to complete the objective by exploiting these vulnerabilities. Whatever the victim needs to do, for the exploit to work, would be simulated by the project. 

The playground is a CTF style application where the objective is to read the flag available for each vulnerablity. Main vulnerability page has detailed information about scenarios & test accounts to be used.

## Demo
Demo video is available at https://youtu.be/8LN56u8RtEY

## Setup Instructions
### Docker
There is a docker available for this. Follow below commands to set it up:
```sh
$ docker pull amolnaik4/bodhi_app
$ docker run -p 80:80 -p 8000:8000 amolnaik4/bodhi_app
```
Once docker is running, access the application at http://<your_machine_ip>
### Using Code
**The code is used to build Docker. It is higly recommended to use Docker. This code can be used as reference. If you want to build it from source, you will need to change code to be able to work.**

Bodhi uses Google Chrome in headless mode with selenium. We need to install Google Chrome & ChromeDriver. Following commands are used for installation on Ubuntu:
```sh
$ mkdir temp
$ cd temp/
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo dpkg -i --force-depends google-chrome-stable_current_amd64.deb
# chromedriver installation
$ wget https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip
$ sudo cp chromedriver /usr/bin/
```

Next steps:
```sh
$ git clone https://github.com/amolnaik4/bodhi.git
$ cd bodhi
$ pip install -r requirements.txt
$ ./run.sh
```
Browse to http://<your_machine_ip>

**Happy Learning !!**
**PRs and more than welcome**
**If you like the project, feel free to join in for beers sometime.**
