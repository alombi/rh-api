module.exports = async(req, res) => {
  data = {}
  data.project = "Unofficial RoutineHub API for retrieving version history of shortcuts."
  data.author = "alombi"
  let style = '<style>*{font-family:system-ui}</style><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>';
  let title = '<h1>Unofficial RoutineHub API</h1>';
  let subtitle = '<p>This project is a serverless API hosted on Vercel that retrieves version history, release notes and other informations about Shortcuts hosted on RoutineHub.'
  let heading = '<h2>How to use</h2>'
  let paragraph = '<p>Heads over to <i>https://rh-api.alombi.xyz/changelog</i> and add a parameter to this URL, containing your shortcut\'s RH ID. For example <a href="https://rh-api.alombi.xyz/changelog?id=1">https://rh-api.alombi.xyz/changelog?id=1</a></p>'
  let subheading = '<h3>Contribute</h3>'
  let subparagraph = '<p>If you want to contribute to the project, report a bug, request a feature or just read the source, check out this GitHub repo: <a></a></p>'
  let footer = '<br>Developed by alombi. © 2021 alombi'
  let html = style + title + subtitle + heading + paragraph + subheading + subparagraph + footer
  res.send(style + html)
}