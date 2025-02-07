## Bloom

Plant information: Databse containing 200 popular plants and their information. 
Humditiy sensing: When a plant's humidity falls outside of its specific threshold, bloom will notify you and trigger automated watering
UI: create and manage personal gardens, access detailed plant care information, and even connect with friends to share and explore their gardens.

***In Progress***

#### Table of Contents
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Features and Use Cases](#Features-and-Use-Cases)
- [Database Schema](#database-schema)
- [Roadmap](#roadmap)


#### Introduction
I created Bloom after struggling to keep my plants alive. The goal is simple: build an application that combines plant management, automation, and community in one platform. Bloom helps you:

- Access detailed care instructions for your plants.
- Automate watering schedules based on plant preferences.
- Track your plant's health, age, and growth.
- Connect with friends to share gardens and plant cuttings.

Bloom started as a personal project to enhance my gardening experience and is now being developed for myself and friends who share a love for plants.


#### Technologies Used
- ESP32 for reading humiditiy senor, acts as Kafka Producer
- Django for the back-end framework 
- React for the front-end framework
- PostgresSQL for the database 
- Docker Container for the PostgresSQL database
- pgAdmin4 for the PostgresSQL database
- API's: Treffle.io
  

#### Features and Use Cases

- Create User profile
- Create personal gardens 
- Create personal plant from database of 40K known plants 
- Add plants to their gardens
- Query information about a plant 
- Add friends 
- Visit friend's Gardens 
- Request a stem or fruit from friend's garden
- Track personal plant age and growth
- Store, search and delete personal plants
- Adjust Garden and plant visibility (public or private)

Future Use Case example: 

I add decided to add my bonsai tree to a Garden named "Sera's Room". I click "create new plant", type in "Bonsai" pick it's type from the search responses. I add it's age, picture and some notes in it's profile. I am able to see the ideal water, soil, sunlight and humidity preferences for this Bonsai! 

I visit my friend's garden and see that she has a medium sized pathos plant! The information under this plant says it can be propagated. I have been wanting a pathos plant so I send a propagation request. 

#### DataBase Schema

Tables:
- **Plants**: Stores plant information (name, family, genus, etc.)
- **Users**: Stores user details and preferences
- **Personal Plants**: Links users to plants with care history
- **Garden**: Stores garden-specific information


#### Roadmap 
Bloom is currently in the early stages of development. 

**Current Progress**
- Created database schema and applied initial migrations.
- Propagated the database with 100 most-popular plants, using Treffle.io API to fetch information
- Connected frontend to back end API's
- Initialized front end development with basic layout and components  

**Upcoming Tasks**
- Iteratively implement functionalities
- Deploy (future)
- Integrated water automation 


