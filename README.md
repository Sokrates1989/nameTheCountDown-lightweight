# nameTheCountDown-lightweight
A lightweight dockerized python telegram bot to create custom countdowns

## Usage

If you just want to use a it as a customer: Simply download telegram and talk to the Bot http://t.me/NameTheCountdownBot 

## Installation

If you want to to install this on your own device to create your own named countdown bot:

And do not worry, the guide looks more frightening than it is, I was just very explicit, so that everyone should be able to follow.

1) Download telegram (best try telegram for windows/mac, It is much easier to interact with your bot)  [https://telegram.org/](https://telegram.org/)
2) Create your own bot talking to the Botfather (and yes it is a bot, to create other bots)  [https://t.me/botfather](https://t.me/botfather) [https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot)
3) Install docker for cli on your host device (QNAP NAS, Synology, Windows, Mac, Linux, ..) [https://www.docker.com/get-started/](https://www.docker.com/get-started/)
4) Download the full repository or make a git clone of this project.
4.1) OPTIONAL: If you want you can edit the password / username in the docker-compose.yml file (If you edit MYSQL_ROOT_PASSWORD, make sure to use the same password for both phpmyadmin and db)
5) cd to the base directory where you copied / pulled this file in step 4. (you have to use a cli for this: powershell, cmd, shell, ssh to your host device using putty or similar)
6) Run the docker compose command. There will be errors, because we must set up the database when it is up. For now we ignore the error, but we need the database up and running. (This might take a while, because it installs alpine, python, pip, mysql and phpmyadmin)
```bash
# to keep it running in the background. 
docker-compose up -d --build 
```

```bash
# to see the console output and to stop the containers by pressing CTRL + C
docker-compose up --build 
```
            
            
7) We will have to setup the database now once. (If you know how to do this automatically with docker / scripts, let me know pls)

7.1) Figure out the ip-address of the device, you copied / pulled the files to in step 4. If you installed it one the same machin it would be 127.0.0.1 or localhost

7.2) Open your browser, that is in the same network as the host device, where you copied/ pulled your files to in step 4.

7.3) Go to the ip address you figured out in step 7.1 on port 8088 (Or the one you gave to the service phpmyadmin in docker-compose.yml). (If you installed it on your own device that would be [127.0.0.1:8088](127.0.0.1:8088) , if you installed it in your local network it would be something as [192.168.x.x:8088](192.168.x.x:8088) ) 
to open phpmyadmin. This is a browser tool, to interact with your database.

7.4) Login with the credentials from step 4.1 (If you did not change them -> use user: root  password: root)

7.5) Create a new database with the name countdown_telegram_bot using collation utf8_unicode_ci

7.6) Create a user just for accessing this database.
    Go to your newly created database.
    Click on privileges in the top menu
    Click on "Add user account" at the bottom
    Best is to create a user with the same name as the database so countdown_telegram_bot and then create or think of a new password.
    Set host to every host (%) and grant all access to just this database (should be automatically chosen, if you used the route database -> privileges, instead of user accounts)

7.7) Import the skeleton database.
    Click on the database again as you started in 7.6.
    Click on import.
    Import countdown_telegram_bot.sql that you can find in the directory install
        you can just drag and drop the file (countdown_telegram_bot.sql) there or use the given buttons.

8) Finally edit the config file (config-.txt) with the newly created information.

8.1) Rename the config.txt.template file to config.txt

8.2)Edit Database  part of the config.txt

    Host: If you havent changed the ip address in the docker-compose.yml keep it like that. (or use the ip adrress of the container db under networks -> namedCountdownNetwork -> ipv4_address, Usually docker supports DNS, but it did not work in connection with the config.txt )

    user: Enter the database user for the database you created in 7.6

    password: Enter the database user password for the database you created in 7.6

    database: If you followed these steps, keep it like that. (Or use the name of the database you created in 7.5)

    port: keep the port (or use the port of docker-compose.yml you can find under db -> ports and db -> expose)

8.3) For the bot token use the token the botfather gave you in step 2

8.4) Save the file


9) Finally (stop and) restart the docker container

10) Your Bot should be working now. You and everyone in the world can create named countdowns when talking to your bot (You can find your bot with the name you gave it in step 2 and by clicking on the t.me link the botfather also gave you in step 2)
    



## License
[MIT](https://choosealicense.com/licenses/mit/)
