# Unofficial RoutineHub API
![](https://img.shields.io/website?down_message=offline&up_message=online&url=https%3A%2F%2Frh-api.alombi.xyz)
![](https://img.shields.io/github/release-date/alombi/rh-api?label=latest%20release)
![](https://img.shields.io/badge/project%20status-active-brightgreen)

rh-api is an unofficial API that scrapes informations about shortcuts hosted on [RoutineHub](https://routinehub.co), the most popular platform for sharing iOS shortcuts. This project tries to create an alternative to the official API using `web scraping` and offering lots of data that aren't available in the current (`V1`) version of the official API. 

The application is built with Next.js and Typescript, and hosted on Vercel.



## Documentation
* [Changelog](#changelog-get)
* [Search](#search-get)
* [Shortcut](#shortcut-get)
* [Author](#author-get)


## Changelog (GET)
The base url is https://rh-api.alombi.xyz/changelog. The **required** parameter to this URL is your shortcut's RH ID. For example https://rh-api.alombi.xyz/changelog?id=1
### Response
* `name` = the name of the shortcut
* `updates` = the number of updates the author made
* `versions` = an array that contains as many elements as the `updates` value. Each element has these parameters:
   * `version` = version number
   * `download_url` = (NEW in 2.0) the url to download the specific version
   * `release_date` = the specific verision's release date
   * `iOS` = the version's supported operating system
   * `release_notes` = the version's release notes
   * `downloads` = the specific version's downloads count

## Search (GET)
The base url is https://rh-api.alombi.xyz/search. The **required** parameter to this URL is your search term. For example https://rh-api.alombi.xyz/search?q=mediakit
### Response
* `results` = contains an array with the search results
   * `name` = the name of the shortcut
   * `id` = the RoutineHub ID of the shortcuts
   * `description` = the shortcut's brief description
   * `downloads` = the shortcut's downloads count
   * `hearts` = the shortcut's hearts count
   * `link` = the link to the shortcut's RoutineHub page
   * `api_url` = the url to the `/shortcut` endpoint
   * `routinehub_api_url` (NEW in 2.0) url to the official API

## Shortcut (GET)
The base url is https://rh-api.alombi.xyz/shortcut.The **required* parameter to this URL is your shortcut's RH ID. For example https://rh-api.alombi.xyz/shortcut?id=1
### Response
* `id` = the RoutineHub ID of the shortcut
* `name` = the shortcut's name
* `description` = the shortcut's brief description
* `hearts` = the total hearts number
* `downloads` = the total downloads number
* `author` = object containing
   * `username` = author's username
   * `page_url` = (NEW in 2.0) url to the author's page on RoutineHub
   * `api_url` = (NEW in 2.0) url to the `/author` endpoint
* `latest_version` = object containing
   * `version` = (NEW in 2.0) latest version
   * `updated` = (NEW in 2.0) date of the last update
* `categories` = an array of minum 1 and maximum 2 elements containing shortcut's categories
* `iOS` = the iOS version the current version of the shortcut is made for
* `download_url` = the shortcut's download url

> `icon` and `related` were removed in 2.0.


## Author (GET)
Heads over to https://rh-api.alombi.xyz/author and add a parameter to this URL, containing the author's RH username. For example https://rh-api.alombi.xyz/author?username=alombi
### Response
* `username` = the author's username
* `avatar` = the link to the profile pic
* `bio` = the author's description (if present)
* `stats` = object containing
   * `total_shortcuts` = the number of authored shortcuts
   * `total_downloads` = the total number of downloads
   * `downloads_average` = the average of downloads
* `contacts` = an object structured like this:
   * `keybase` = link
   * `twitter` = link
   * `facebook` = link
   * `reddit` = link
   * `youtube` = link
   * `github` = link
   * `gitlab` = link
   * `website` = link
* `isMember` = a boolean that indicates if the user is a member (`true`) or not (`false`)
* `isMod` = a boolean that indicates if the user is a mod (`true`) or not (`false`)

> `total_hearts` and `hearts_average` were removed in 2.0