# Datamining

This project involves collecting detailed information about music albums and their reviews from Metacritic using a tool called Scrapy. It starts by creating a program called a "spider" to go through the website and grab information like the album name, its Metascore, user scores, the genre, release date, artist name, and the record label from each album page. It also picks up reviews from critics, including their names, scores, dates, and the text of their reviews.

After gathering all this information, the next step is to organize and clean up the data. This includes sorting out the genres and giving each one a unique ID, making the data easier to work with. The project uses a library called pandas for this part, which helps in breaking down the critics' reviews into separate entries to keep the data neat and orderly.

Once the data is all cleaned up, it's uploaded into a PostgreSQL database. This database is set up with different sections for artists, albums, reviews, genres, and how all these elements are connected. This setup makes it easy to search through the data and pull out whatever information is needed, whether for analysis or building something new with the data.
