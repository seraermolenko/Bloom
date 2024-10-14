## Bloom
Are you curious about what plants your friends have? Do you struggle to keep your plants alive? Bloom is a web-based plant management application designed to help users create and manage personal gardens as-well as visit their friend's gardens.  

***In Progress***

#### Table of Contents
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Features and Use Cases](#Features-and-Use-Cases)
- [Database Schema](#database-schema)
- [Roadmap](#roadmap)


#### Introduction
My plants kept dying I decided to create an application that will make my gardening life, interesting and easier. My goal was to develop something that can easily give you information about your plant, store your plants and automate the watering tasks. This application is being developed for myself and a few friends.

#### Technologies Used
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
- Propagated the database suing Treffle.io API to fetch information
- Connected frontend to back end API's
- Initialized front end development with basic layout and components  

**Upcoming Tasks**
- Complete UI
- Add user authentication (Oauth2)
- Iteratively implement functionalities
- Deploy 


