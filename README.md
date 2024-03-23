### steps to follow for running the application

1. create a empty directory and `cd` into that directory
2. run `git clone https://github.com/ttejas16/resume-builder.git .` to clone the repository
3. run `pip install -r requirements.txt` to install required dependencies/packages
4. create a actual `.env` file inside the `resume_buidler` directory with the same 
   variable names as specified in `example_env.txt`
5. run `flask --app resume_builder --debug run` to start the application
6. access the site at `http://127.0.0.1:5000` 