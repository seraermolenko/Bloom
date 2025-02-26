## Bloom
#### Table of Contents
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Database Schema](#database-schema)
- [Roadmap](#roadmap)

#### Introduction

I created Bloom after struggling to keep my plants alive. The goal is simple: build an application that combines plant management, information, and automation. This project was also driven by desire to learn new tools and concepts, ranging from containerization and data streaming to working with sensor drivers. 

Quick summary: 
Bloom has a database containing 200 popular plants and their information. An ESP32 streams values from a humidity sensor monitors my plant's soil level. When this value is outside of the specific plant's threshold, a warning is sent. 

Humidity Sensor Driver -> ESP32 ->  POST request -> sends data to kafka broker ->  consumer 

- *ESP32 producer is defined in another repository called Humidity* 
- *Watering notification is triggered by values outside of the specific threshold that is set based on treffle.io's plant data*

Soon to come:
My next step is to keep learning React so that I can create a UI.
Eventually, Bloom could offer
- Access to detailed care instructions for plants.
- Automate watering schedules based on plant preferences.
- Tracking plant's health, age, and growth.
- Connecting with friends to share gardens and plant cuttings.


#### Technologies Used
- PostgresSQL for the database 
- ESP32 for the microcontroller 
- DHT11 for the humidity sensor
- Docker Volume for the PostgresSQL database
- Django for the back-end framework 
- React for the front-end framework
- pgAdmin4 for database management 
- Postman for API testing 
- API's: Treffle.io  

#### DataBase Schema

Tables:
- **Plants**: Stores plant information (name, family, genus, etc.)
- **Users**: (soon to come) Stores user details and preferences
- **Personal Plants**: Links users to plants with care history
- **Garden**: Stores garden-specific information

![databaseSnapshot](images/pgSnapshot.png)


#### Roadmap 

Current Progress
- Created database schema
- Propagated the database with 100 most-popular plants, using Treffle.io API to fetch information
- Connected frontend to backend API's
- Created a kafka topic and established a connection between producer/consumer

Upcoming Tasks
- Iteratively implement functionalities
- Deploy (future)
- Integrated water automation 