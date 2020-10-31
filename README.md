# Ideco Python Developer Test Task

## Description

Implement __Aiohttp web app__ with the following conditions:

* Web app on port 8080

* Output logs to stdout 

* Web app run works inside Docker 
    * `Dockerfile` based on feadora:32
    * Use [Kernel Vanilla Repositories](https://fedoraproject.org/wiki/Kernel_Vanilla_Repositories)

* We have two files `news.json` with list of news and `comments.json` with comments on news.

* __API__ with to methods:

    * __(GET) /api__, return list of news with the following requirements

        * All _news_ sorts by field `date` (format ISO 8601)
        * Return only not deleted news , check field `deleted`
        * Do not return news for these creation time has not come yet
        * Return comments count for each news

    * __(GET) /api/news/{id}__, return news by _id_ with comments

        * Return comments for this news. All _comments_ sorted by field `date`  (format ISO 8601)
        * Return only no deleted news , check field `deleted`
        * If news with the following _id_ deleted field `deleted` then return error code 404 
        * If news creation time has not come yet then return error code 404 

    * __(POST) /api/news__, add new news by _id_
    * __(DELETE) /api/news/{id}__, delete news by _id_

* All notes stored in `json`.

## Implementation

* In this nask we have no frontend. And we will return __Json__ responses to our requests.

* In this task we have no database. We use json files in folder _data_ for storing data.

* We sort news and comments in order from newest to oldest.

* Return Json responses.

* Еhe current task didn't need to run our application on a web server (e.g. nginx). Therefore, we run our application in a docker container without additional settings.

## Docker

* Open terminal

* Pull image from Docker Hub
```
sudo docker pull margarita9/test_task_aiohttp:second
```
* Run 
```
sudo docker run --publish 8080:8080 margarita9/test_task_aiohttp:second
```
* Go to browser and run http://0.0.0.0:8080/api

## Examples of result

* Open another terminal

* Check __(GET) /api__

```
> curl http://0.0.0.0:8080/api

> {"news": [{"id": 1, "title": "news_1", "date": "2019-01-01T20:56:35", "body": "The news", "deleted": false, "comments_count": 1}], "news_count": 1}
```

* Check __(GET) /api/news/{id}__

```
> curl http://0.0.0.0:8080/api/news/1

> {"id": 1, "title": "news_1", "date": "2019-01-01T20:56:35", "body": "The news", "deleted": false, "comments": [{"id": 1, "news_id": 1, "title": "comment_1", "date": "2019-01-02T21:58:25", "comment": "Comment"}], "comments_count": 1}
```

* Check __(POST) /api/news__

```
> curl -X POST -H "Content-Type: application/json" -d '{"id":2,"title":"news_2","body":"The news","comments":[{"id":1,"news_id":2,"title":"comment_1","comment":"Comment"}]}' http://0.0.0.0:8080/api/news

> 200: OK

> curl http://0.0.0.0:8080/api

> {"news": [{"id": 2, "title": "news_2", "body": "The news", "deleted": false, "date": "2020-10-31T17:35:54", "comments_count": 1}, {"id": 1, "title": "news_1", "date": "2019-01-01T20:56:35", "body": "The news", "deleted": false, "comments_count": 1}], "news_count": 2}

```

* Check __(DELETE) /api/news/{id}__

```
> curl -X DELETE http://0.0.0.0:8080/api/news/2

> 200: OK

> curl http://0.0.0.0:8080/api
(shows only not deleted news)

> {"news": [{"id": 1, "title": "news_1", "date": "2019-01-01T20:56:35", "body": "The news", "deleted": false, "comments_count": 1}], "news_count": 1} 

```
