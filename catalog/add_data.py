# Required modules are imported to this file

from db_create import Base, Branch, Course, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

#engine = create_engine('sqlite:///branchcourse.db')
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Get Current date
current_date = str(datetime.date.today())
# Create dummy user

User1 = User(name="Narayana", email="satyanarayana0099@gmail.com",
             picture="https://plus.google.com/u/0/photos/102218847128353529116/\
  albums/profile/6639738781308160098?iso=false")
session.add(User1)
session.commit()

# Branch-1 [computer science]

cse = Branch(name="Computer Science", user_id=1)
session.add(cse)
session.commit()

# Indian Curreny symbol for ctrl+alt+4 in keyboard
# Branch-1 computer science[python for everybody[var:cse]] Details
fy4e_des = "The Python for Everybody course and "\
           "will introduce fundamental programming concepts "\
           "including data structures, networked application "\
           "program interfaces, and databases, using the Python "\
           "programming language. In the Capstone Project, "\
           "you’ll use the technologies learned throughout the "\
           "Specialization to design and create your own "\
           "applications for data retrieval, processing, and "\
           "visualization."
pythonforeverybody = Course(name="Python For Everybody",
                            description=fy4e_des,
                            date=current_date,
                            image="https://pbs.twimg.com/media"
                                  "/Chy32ozVAAAngk5.jpg",
                            level="Begineer Lavel",
                            price="₹3,406",
                            user_id=1,
                            branch_id=1)

session.add(pythonforeverybody)
session.commit()

# Branch-1 computer science[Java Programming Basics[var:cse]] Details
# Refered Link: https://in.udacity.com/course/java-programming-basics--ud282
java_p_b = "Taking this course will provide "\
    "you with a basic foundation in Java syntax, which "\
    "is the first step towards becoming a successful Java "\
    "developer. You’ll learn how computers make decisions "\
    "and how Java keeps track of information through variables "\
    "and data types. You’ll learn to create conditional "\
    "statements, functions, and loops to process information "\
    "and solve problems. You’ll even learn to use IntelliJ, a "\
    "Java IDE (Integrated Development Environment) that "\
    "professional developers use, to build, compile, and debug "\
    "your code. These are foundational programming skills, and "\
    "mastering them is a must for all aspiring programmers.",
javaProgrammingBasics = Course(
    name="Java Programming Basics",
    description=java_p_b[0],
    date=current_date,
    image="http://www.techpresentations.org/myphoto/f/7/747"
          "14_java-programming-wallpaper.jpg",
    level="Begineer Lavel",
    price="₹ Free",
    branch=cse,
    user_id=1, branch_id=1)
session.add(javaProgrammingBasics)
session.commit()

# Branch-2 [Electronics and communication Engineering]

ece = Branch(name="Electronics and Communication", user_id=1)
session.add(ece)
session.commit()

# Branch-2 Electronics and communication[Introduction to Electronics
# Referrenced from https://www.coursera.org/learn/electronics

Electronics = Course(name="Introduction to Electronics ",
                     description="This course introduces"
                     "students to the basic components of"
                     "electronics: diodes, transistors, "
                     "and op amps. It covers the basic "
                     "operation and some common applications.",
                     date=current_date,
                     image="http://silver-fox.ca/electronixheader1.gif",
                     level="Begineer Lavel",
                     price="₹2,000",
                     branch=ece,
                     user_id=1,
                     branch_id=2)
session.add(Electronics)
session.commit()

# Branch-2 Electrical and Electronics[Internet of Things]
# Referrenced from https://www.coursera.org/specializations/internet-of-things
iot_des = "This Specialization covers the development"
"of Internet of Things (IoT) products and services—including devices"
"for sensing,actuation, processing, and communication—to help you "
"develop skills and experiences you can employ in designing novel "
"systems. The Specialization has theory and lab sections. In the "
"lab sections you will learn hands-on IoT concepts such as "
"sensing, actuation and communication. In the final Capstone Project,"
"developed in partnership with Qualcomm, you’ll apply the skills you "
"learned on a project of your choice using the DragonBoard 410c platform."
iot = Course(name="Internet of Things (IOT) ",
             description=iot_des,
             date=current_date,
             image="https://www.houseofbots.com/images/news/3721/cover.png",
             level="Begineer Lavel",
             price="₹3,406",
             branch=ece,
             user_id=1, branch_id=2)
session.add(iot)
session.commit()

# Branch-3 Electronics and communication[Internet of Things [var:ece]] Details

eee = Branch(name="Electrical and Electronics", user_id=1)
session.add(eee)
session.commit()

# Branch-3 Course-1 Details
# Refferenced from https://www.coursera.org/degrees/msee-boulder

MasSciElectrical = Course(name="Master of Science in Electrical Engineering",
                          description="Take a big step and advance your \
career with the Master of Science in Electrical Engineering program from \
the University of Colorado Boulder. CU Boulder is ranked as the 38th best \
school in the world by the Academic Ranking of World Universities. The \
Master of Science in Electrical Engineering teaches foundational knowledge,\
applied skills, and the latest technological developments in embedded \
systems, power electronics, photonics, and more.",
                          date=current_date,
                          image="https://cdn.wallpapersafari.com/72/2/7uvxX5"
                          ".jpg",
                          level="Begineer Lavel",
                          price="₹30,000",
                          branch=eee,
                          user_id=1,
                          branch_id=3)
session.add(MasSciElectrical)
session.commit()

# Branch-3  Course-2 Electrical  Engineering
# Referrenced from https://www.coursera.org/specializations/power-electronics?

PowerElectronics = Course(name="Power Electronics",
                          description="Design modern switched-mode power \
converters; create high-performance control loops around power converters; \
understand efficiency, power density and cost trade-offs",
                          date=current_date,
                          image="https://previews.123rf.com/images/kran7"
                          "7/kran771412/kran77141200080/34873369-abstract-"
                          "electric-circuit-digital-brain-technology-concept"
                          ".jpg",
                          level="Intermediate Level",
                          price="₹5,000",
                          branch=eee,
                          user_id=1, branch_id=3)
session.add(PowerElectronics)
session.commit()

# Branch-4 [Mechanical Engineering]

mec = Branch(name="Mechanical", user_id=1)
session.add(mec)
session.commit()

# Branch-4 Mechanical Engineering[Introduction to Engineering Mechanics
# Refferenced from https://www.coursera.org/learn/engineering-mechanics-statics
IntEnMe_des = "This course is an introduction to learning and applying the "\
              "principles required to solve engineering mechanics problems. "\
              "Concepts will be applied in this course from previous"\
              "courses you have taken in basic math and physics.  The course "\
              "addresses the modeling and analysis of static equilibrium "\
              "problems with an emphasis on real world engineering "\
              "applications and problem solving."
IntroductionEngineeringMechanics = Course(name="Introduction to\
  Engineering Mechanics",
                                          description=IntEnMe_des,
                                          date=current_date,
                                          image="https://wallup.net/wp-content"
                                          "/uploads/2017/03/27/74712-artwork-"
                                          "mechanics.jpg",
                                          level="Intermediate Level",
                                          price="₹4,500",
                                          branch=mec,
                                          user_id=1, branch_id=4)
session.add(IntroductionEngineeringMechanics)
session.commit()

print("Branches & Courses are added to Database Sucessfully.")
