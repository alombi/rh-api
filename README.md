# Unofficial RoutineHub API
![](https://img.shields.io/website?down_message=offline&up_message=online&url=https%3A%2F%2Frh-api.alombi.xyz)
![](https://img.shields.io/github/release-date/alombi/rh-api?label=latest%20release)
![](https://img.shields.io/badge/project%20status-active-brightgreen)

This project is a serverless API hosted on Vercel that retrieves some useful informations that aren't available from the official API (yet) about Shortcuts hosted on [RoutineHub](https://routinehub.co).

> The homepage endpoint has been deprecated due to the removal of trending shortcuts on RoutineHub homepage.


## Documentation
* [Changelog](#changelog-get)
* [Search](#search-get)
* [Shortcut](#shortcut-get)
* [Author](#author-get)
<!-- * ~~[Homepage](#homepage-get)~~ -->


## Changelog (GET)
Heads over to https://rh-api.alombi.xyz/changelog and add a parameter to this URL, containing your shortcut's RH ID. For example https://rh-api.alombi.xyz/changelog?id=1
### Response
* `id` = the shortcut's id
* `name` = the name of the shortcut
* `toalUpdates` = the number of updates the author made
* `versions` = an array that contains as many elements as the `toalUpdates` value. Each element has these parameters:
   * `version` = version number
   * `download_link` = (NEW) the specific version's download link 
   * `release_date` = the specific verision's release date
   * `iOS` = the version's supported operating system
   * `release_notes` = the version's release notes
   * `downloads` = the specific version's downloads count

## Search (GET)
Heads over to https://rh-api.alombi.xyz/search and add a parameter to this URL, containing your search term. For example https://rh-api.alombi.xyz/search?q=mediakit
### Response
* `results` = contains an array with the search results
   * `name` = the name of the shortcut
   * `id` = the RoutineHub ID of the shortcuts
   * `description` = the shortcut's brief description
   * `downloads` = the shortcut's downloads count
   * `hearts` = the shortcut's hearts count
   * `link` = the link to the shortcut's RoutineHub page
   * `api_link` = the link to the `/shortcut` endpoint

## Shortcut (GET)
Heads over to https://rh-api.alombi.xyz/shortcut and add a parameter to this URL, containing your shortcut's RH ID. For example https://rh-api.alombi.xyz/shortcut?id=1&icon=true
### Response
* `id` = the RoutineHub ID of the shortcut
* `name` = the shortcut's name
* `description` = the shortcut's brief description
* `hearts` = the total hearts number
* `downloads` = the total downloads number
* `icon` = the shortcut's icon (base64 encoded). Not included by default.
* `author` = the shortcut's author username
* `categories` = an array of minum 1 and maximum 2 elements containing shortcut's categories
* `related` = an array with 2 or 3 shortcuts that are related to the shortcut. This parameter includes a shortcut authored by the same user and one from each category of the shortcut. Not included by default. 
#### Icon
The `icon` url parameter is `false` by default, and it's optional. If you want to receive the icon, include it as in the example (https://rh-api.alombi.xyz/shortcut?id=1&icon=true), if not set it to `false` or remove the parameter.

#### Related 
The `related` parameter is `false` by default, and it's optional. If you want to receive related shortcuts, include it as in the example (https://rh-api.alombi.xyz/shortcut?id=1&related=true), if not set it to `false` or remove the parameter. Take note that requesting related shortcuts may slow down the process a bit.


## Author (GET)
Heads over to https://rh-api.alombi.xyz/author and add a parameter to this URL, containing the author's RH username. For example https://rh-api.alombi.xyz/author?username=alombi
### Response
* `username` = the author's username
* `avatar` = the link to the profile pic
* `bio` = the author's description (if present)
* `total_shortcuts` = the number of authored shortcuts
* `total_downloads` = the total number of downloads
* `total_hearts` = the total number of hearts
* `downloads_average` = the average of downloads
* `hearts_average`  = the average of hearts
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

<!-- ## Homepage (GET)

~~Heads over to https://rh-api.alombi.xyz/homepage~~
### ~~Response~~
* ~~`trending` = an array containing 6 elements~~
* ~~`new` = an array containing 6 elements~~
* ~~`recently-updated` = an array containing 6 elements~~

~~Each array has the same elements' structure:~~
* ~~`name` = the name of the shortcut~~
* ~~`id` = the RoutineHub ID of the shortcuts~~
* ~~`description` = the shortcut's brief description~~
* ~~`downloads` = the shortcut's downloads count~~
* ~~`hearts` = the shortcut's hearts count~~
* ~~`link` = the link to the shortcut's RoutineHub page~~
* ~~`api_link` = the link to the `/shortcut` endpoint~~ -->