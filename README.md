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

* In this task we have no database. We use to json files in folder data for storing data.

* We sort news and comments in order from newest to oldest.

* 

## Content of the project 



## Web paths



## How to run 



## Docker

