# Online Courses App  
## Developed by Naga Satyanarayana Mutta	
This is one of the project for the Udacity [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## About Project:
This project display the different types of courses those courses are available in online with related to different types of Engineerings, Any user can visit this courses but only authenticated user can add an course or branch, edit and delete operations are possible.

## Skills Required:
   * Python
   * Html5
   * CSS
   * Flask FrameWork
   * OAuth
   * SQLAlchemy
  
## How to Install :

    Step 1 ==> Install [Python](https://www.python.org/downloads)
    
    Step 2 ==> Install [Vagrant](https://www.vagrantup.com/downloads.html)
    
    Step 3 ==> Install [VirtualBox](https://www.virtualbox.org/wiki/downloads)
    
    Step 4 ==> Install [Git](https://git-scm.com/download/win) --> For Windows
    
    Step 5 ==> Launch the vagrant virtual machine inside vagrant sub-directory then open Git Bash: `$vagrant up`
    
    Step 6 ==> Login to vagrant virtual machine --> `$vagrant ssh`
    
    Step 7 ==> Change directory to /vagrant --> `$cd /vagrant/`
    
    Step 8 ==>  Change directory to  Projectors project folder inside vagrant folder--> `$cd Online Courses App`
    
    Step 9 ==> Install the requirement project modules are:
    
        * `sudo pip install flask`
        * `sudo pip install oauth2client`
        * `sudo pip install sqlalchemy`
        * `sudo pip install requests`
    
     Step 9 ==> Create application database:`$python3 db_create.py`
    
     Step 10 ==> Inserting application data in database -->`$python3 add_data.py`

     Step 11 ==> Run the main project file -->`python3 app.py`
    
     Step 12 ==> Access the application any local browser[http://localhost:5000](http://localhost:5000)

 ### JSON EndPoints: In this project we create json endpoints using REST architecture

 1) Display the all Categories with Items : `http://localhost:5000/courses/JSON`

 2) Display the items of given category: `http://localhost:5000/branches/1/JSON`

 3) Display the all Categories : `http://localhost:5000/branches/JSON`

 4) Display single item : `http://localhost:5000/course/1/1/JSON`
 












