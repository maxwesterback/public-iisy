# public-iisy

IISY is a student project which ended up as a project accepted into a startup program but we ended up abandoning it due to our team lacking in knowledge to make this into a 'real' 
commercial product. The target customer would be mainly things like universities or offices where there are a lot of different products which could experience a myriad of different issues.
The maintenance team responsible would for example create 30 QR codes with the category of Computer which all link to a unique webpage with the option to send a message to the 
team that the specific Computer is having an issue. When they install the QR codes they first scan them and then go to the settings page in which they can enter the location 
of the Computer and who should get an email when people report an issue. This way the people who report the issue only need the camera app on their phone and they don't 
need to know who to send the issue to or even where they are. The User guide which I wrote goes through the setup for a customer.

On our side the system is built on the Django tenant system which means that every new customer gets their own version of the schema but all the schemas share a database. Think of the 
Database as an apartment building and the Customer gets their own apartment which is identical to all other apartments and the apartment is obviously the iisy_landing app with its own schema. This makes it 
really easy for us to get one Customer set up to use the system quickly and it's impossible for them to access another Customers information. Having only one database also keeps 
costs and maintenance down to a minimum

I'm responsible for all the code except for the static folder, chart.html, index.html in home_app and company_page but of course the entire team had influence on what features we added. I'm also the one who hosted the application on Heroku 

Things you need to make this project work locally:

1. General knowledge of Django framework
2. Install a PostgreSQL server
3. Update the database information in SETTINGS
4. Update Views.py in IISY_LANDING, specifically the register_ticket method on lines 83 and 120. Replace newdomain.live/admin/iisy_landing with localhost or however you want to host the application
5. Install all the requirements and follow the setup.txt and then the user guide. Potentially the Django_tenants text file if you want a better understanding of tenants
6. Makemigrations and migrate to your server and afterwards you should hopefully be able to run the project. Otherwise idk haven't touched this in a long while
