### steps to follow for running the application

### for those who want to create a new folder
1. install postgres database locally
2. find your password :p
3. create a DATABASE(not table) named `resume`

ignore the above commands if created ☝️

4. create a empty directory and `cd` into that directory
5. run `git clone https://github.com/ttejas16/resume-builder.git .` to clone the repository
6. after that create a `.env` file inside `resume_builder` directory 
7. add all the variables specified in the `resume_builder/example_env.txt` to the newly created `.env` file
8. save and run `pip install -r requirements.txt` to install required dependencies/packages
9. save and run the application using command `flask --app resume_builder --debug run`
10. access the site at `http://127.0.0.1:5000`


### for those who want to use their existing folder
1. install postgres database locally
2. find your password :p
3. create a DATABASE(not table) named `resume`

ignore the above commands if created ☝️

4. fetch changes(if any) from github using the command `git pull origin main`
5. after the changes are reflected, create a `.env` file inside `resume_builder` directory 
6. add all the variables specified in the `resume_builder/example_env.txt` to the newly created `.env` file
7. save and run the application using command `flask --app resume_builder --debug run`
8. access the site at `http://127.0.0.1:5000`  