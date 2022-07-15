# NBS Web Crawler

This project was made to extract, parse and store data from articles. It also offers
a few different API endpoints to interact with the database.


## Configuration

- the USER-AGENT has been set to 'v.dimitrov (+https://github.com/m1xedstw)'
- the crawler will respect the ```robots.txt``` file
- the spider log is saved in the ```'output.log'``` file
- The log level is set to 'INFO' - debugging messages are not shown

## More info about the spider

The spider uses a hidden API to fetch article URLs from the NBS domain. The response
is then validated against a JSON schema file ```/spiders/schema.json```. If the validation
is successful, it proceeds by following each one of the fetched URLs and extracts a few
datapoints for each article:
- Title
- Date
- Link
- Labels
- Text(body) of the article

For each article, an ```ArticlesItem()``` object is created. It is then sent to the Item
Pipeline, where:

- its structure is validated against a JSON schema using the ```Spidermon``` framework.
- its data is stored in SQLite3 database

The database has a UNIQUE constraint on the 'link' column to prevent duplicate entries.

## More info about the API

- Uses SQLAlchemy models to interact with the database
- Uses Pydantic models to validate the output
- Each request gets its own database connection session through the 
  SessionLocal() class and creating a dependency (https://fastapi.tiangolo.com/tutorial/dependencies/)
- Both GET method should return the data in JSON format and 200 status code
- The DELETE method returns status code 204 and an empty body
- Trying to GET / DELETE a non-existing item should return status code 404

-- Also includes 4 unit tests for API endpoints, located in ```/api/tests``` folder. To test, 
you first need to run:

```bash
  $ pip install pytest
```

as PyTest is not included in the requirements.txt file. Then from the project ```/api/``` folder run:

```bash
  $ python -m pytest
```


## How to use the crawler:

Clone the project

```bash
  $ git clone https://github.com/m1xedstw/NBSCrawler
```

Go to the project directory

```bash
 $ cd NBSCrawler
```

Install dependencies

```bash
  $ pip install -r requirements.txt
```

Navigate to the /spiders/ folder and run the *article* spider:


```bash
  $ cd articles/spiders
  $ scrapy crawl article 
```







## How to run a local server and test the API:

Navigate to the /api/ folder

```bash
  $ cd api
```

Then run the live server:

```bash
  $ uvicorn main:app
```

Send a request to one of the endpoints, for example:

```bash
  $ curl http://127.0.0.1:8000/item/1
```
## API Reference

#### Get all available articles

```http
  GET /items
```



#### Get specific article by ID

```http
  GET /item/{item_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `item_id`      | `integer` | **Required**. Internal ID of the article |



#### Delete article by ID

```http
  DELETE /item/{item_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `item_id`      | `integer` | **Required**. Internal ID of the article |


## Badges

![GitHub total lines](https://img.shields.io/tokei/lines/github/m1xedstw/NBSCrawler) 

![GitHub last commit](https://img.shields.io/github/last-commit/m1xedstw/nbscrawler) 

![GitHub watchers](https://img.shields.io/github/watchers/m1xedstw/nbscrawler?style=social)

![GitHub forks](https://img.shields.io/github/forks/m1xedstw/nbscrawler?style=social)
## Author

- [@v.dimitrov](https://www.github.com/m1xedstw)


## Feedback

If you have any feedback, please reach out to: global.dc@mail.bg
