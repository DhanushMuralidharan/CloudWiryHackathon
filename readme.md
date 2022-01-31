
# CloudWiry Hackathon 2022 - BLOB File Server

## Getting Started..

Welcome to my repository that contains the code base for this hackathon!

To get this codebase working,

 1. Clone into the current repository
 2. Install all the necessary requirements with reference to **requirements.txt**
 3. Run the file **App/main.py** using the command *"python App/main.py"*. This should get the Web App Server up and running!
 4. On a separate terminal, Run the command *"uvicorn API/main:app --reload"*. This should start the API server.
 5. Now, that both the servers are up and running, go to the url provided by flask. (http://127.0.0.1:8001/)
 6. You are good to go!


## Project Overview
The Application contains 3 layers in total.

 1. **Database:** The deepest layer. Contains all the relevant data. In this project I have used SQLite for the ease of demonstration. For production, I would rather recommend a more powerful database such as PostgreSQL or MySQL. We have two entities of interest, one is *User* and the other is *File*.

 2. **API:** The layer that acts as a mediator between the Database and Applications. On the front, it interfaces with a variety of applications such as Web applications, Command Line applications, Applications built on various platforms. But here, we only have the web application implemented. The API listens to requests from these applications and queries the database and returns whatever is being asked for.
 
 3. **Web Application:** The application that directly interacts with the user. Since this is the layer that comes into direct contact with the user, it has to be implemented with utmost caution! It takes care of encryption, authorisation, authentication and does not allow tresspassers to mess with the data!

## Key Features

 Anyone who passes by this web application can *create an account* for themselves

Once a user is authenticated, they can,

 - **Upload New files:** One can upload files of any type which includes but not limited to, .txt,.c,.php,.py,.html,.pdf etc!
 - **Rename existing files:** Files that already exist in the database can be renamed with no effort!
 - **Delete files:** You can permanently remove files from the database. But watch out! We don't do recycle bin, trash here!

*Note: The application allows you to have multiple files with the same file names. As long as you are able to identify them, we are good!*

	 


