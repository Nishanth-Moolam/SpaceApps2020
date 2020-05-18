# SpaceApps2020

This is my repo for the Space Apps 2020 Challenge! I am choosing the Human Factors challenge.

My plan is to scrape data from a number of sources from which I will make an AI model to predict 
the best and worse case future model for a city given certain factors. The challenge asks to 
identify new factors that contribute to the spread of COVID

My plan is to find data for the 100 largest cites in the world including the following factors:
- population
- COVID-19 information since January
- Socioeconomic Status
- Population Movement
- Population Density
- Climate
- Age Distribution
- Government Subsidy given
- Unemployment rate
- Tests administered

Data sources: 
- https://www.worldometers.info/world-population/population-by-country/
- https://www.worldometers.info/coronavirus/

Libraries :
- sqlite3
- pandas
- BeautifulSoup
- urllib.request
- tensorflow
- numpy
- matplotlib


Machine Learning Model from Scratch:
- Define adequately our problem (objective, desired outputs…).
- Gather data.
- Choose a measure of success.
- Set an evaluation protocol and the different protocols available.
- Prepare the data (dealing with missing values, with categorial values…).
- Spilit correctly the data.
- Differentiate between over and underfitting, defining what they are and explaining the best ways to avoid them.
- An overview of how a model learns.
- What is regularization and when is appropiate to use it.
- Develop a benchmark model.
- Choose an adequate model and tune it to get the best performance possible.
