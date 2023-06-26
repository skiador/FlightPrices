##Readme

#Project Overview

The objective of this project is to discover patterns in airline flight pricing. The project includes a scraper that can extract information on flights from the Vueling Airline for any desired route. Additionally, it provides an SQL script to create the required database and a Jupyter Notebook for analysis purposes.

#Configuration

Before using the project, follow these steps for configuration:
    Install the required packages included in the reuqirements.txt
    Set up the SQL database:
        Run the script provided in the \src directory to create the necessary database structure.
    Configure the scrapper:
        Edit the config.ini file and fill in the required parameters to allow the scrapper to connect to the database.
        In the same config.ini file, specify the desired routes by setting the base airport and the airports of interest. For example, if the base airport is Barcelona and the airports of interest are Madrid and Málaga, the scrapper will retrieve information on all the flight combinations between those airports.

#Usage

To use the project:

    Run the scrapper:
        Execute the scrapper script to start extracting flight information from the Vueling Airline based on the configured routes.
    Analyze the data:
        Open the provided Jupyter Notebook to perform analysis on the collected flight data. Use this to discover patterns and insights related to airline flight pricing.


#Contributing

Feel free to contribute to this project.

#Troubleshooting

If you encounter any issues contact me at gerardpalomo88@gmail.com