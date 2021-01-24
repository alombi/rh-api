# Unofficial RoutineHub API
This project is a serverless API hosted on Vercel that retrieves some useful informations that aren't available from the official API (yet) about Shortcuts hosted on RoutineHub.
## Documentation
* [Homepage](https://github.com/alombi/rh-api/blob/master/README.md#homepage-get)
* [Changelog](https://github.com/alombi/rh-api/blob/master/README.md#changelog-get)
* [Shortcut](https://github.com/alombi/rh-api/blob/master/README.md#shortcut-get)
* [Author](https://github.com/alombi/rh-api/blob/master/README.md#author-get)


## Homepage (GET)
Heads over to https://rh-api.alombi.xyz/homepage
#### Parameters
* `trending` = an array containing 6 elements
* `new` = an array containing 6 elements
* `recently-updated` = an array containing 6 elements

Each array has the same elements' structure:
* `name` = the name of the shortcut
* `id` = the RoutineHub ID of the shortcuts
* `description` = the shortcut's brief description
* `downloads` = the shortcut's downloads count
* `hearts` = the shortcut's hearts count
* `link` = the link to the shortcut's RoutineHub page
* `api_link` = the link to the `/shortcut` endpoint

## Changelog (GET)
Heads over to https://rh-api.alombi.xyz/changelog and add a parameter to this URL, containing your shortcut's RH ID. For example https://rh-api.alombi.xyz/changelog?id=1
#### Parameters
* `name` = the name of the shortcut
* `updates` = the number of updates the author made
* `versions` = an array that contains as many elements as the `updates` value. Each element has these parameters:
   * `version` = version number
   * `release_date` = the specific verision's release date
   * `iOS` = the version's supported operating system
   * `release_notes` = the version's release notes
   * `downloads` = the specific version's downloads count

## Shortcut (GET)
Heads over to https://rh-api.alombi.xyz/shortcut and add a parameter to this URL, containing your shortcut's RH ID. For example https://rh-api.alombi.xyz/shortcut?id=1
#### Parameters
* `id` = the RoutineHub ID of the shortcut
* `hearts` = the total hearts number
* `downloads` = the total downloads number

## Author (GET)
Heads over to https://rh-api.alombi.xyz/author and add a parameter to this URL, containing the author's RH username. For example https://rh-api.alombi.xyz/author?username=alombi
#### Parameters
* `username` = the author's username
* `avatar` = the link to the profile pic
* `bio` = the author's description (if present)
* `total_shortcuts` = the number of authored shortcuts
* `total_downloads` = the total number of downloads
* `total_hearts` = the total number of hearts
* `downloads_average` = the average of downloads
* `hearts_average`  = the average of hearts