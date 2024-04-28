const set_time = (id, now) => {
    var utcString = now.toISOString().substring(0, 19)
    var year = now.getFullYear()
    var month = now.getMonth() + 1
    var day = now.getDate()
    var hour = now.getHours()
    var minute = now.getMinutes()
    var second = now.getSeconds()
    var localDatetime = year + "-" +
        (month < 10 ? "0" + month.toString() : month) + "-" +
        (day < 10 ? "0" + day.toString() : day) + "T" +
        (hour < 10 ? "0" + hour.toString() : hour) + ":" +
        (minute < 10 ? "0" + minute.toString() : minute) +
        utcString.substring(16, 19)
    var datetimeField = document.getElementById(id)
    datetimeField.value = localDatetime
}

const init_datetime_field = () => {
    var now = new Date()
    set_time("min-creation-time-seconds", new Date(now - 60 * 60 * 24 * 1000))
    set_time("max-creation-time-seconds", now)
}

const view_protocol = async () => {
    let div = document.getElementById("result-protocol")
    div.innerHTML = ""

    let min = document.getElementById("min-creation-time-seconds").value
    let max = document.getElementById("max-creation-time-seconds").value

    let min_creation_time_seconds = null
    let max_creation_time_seconds = null

    let url = "/etr/api/submissions/?"

    if (min != "") {
        min_creation_time_seconds = +new Date(min)
        url += `min_creation_time_seconds=${Math.floor(Number(min_creation_time_seconds) / 1000)}&`
    }
    if (max != "") {
        max_creation_time_seconds = +new Date(max)
        url += `max_creation_time_seconds=${Math.floor(Number(max_creation_time_seconds) / 1000)}&`
    }

    let response = await fetch(url)

    if (!response.ok) {
        div.innerHTML = `<h1>Ошибка, попробуйте позже.</h1>`
        return
    }

    let data = await response.json()

    let tr
    let cell
    let table = document.createElement("table")
    table.classList = "table table-striped table-hover table-responsive"
    let header = document.createElement("thead")
    header.className = "table-dark"
    tr = document.createElement("tr")
    cell = document.createElement("th")
    cell.innerHTML = "id"
    tr.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = "когда"
    tr.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = "кто"
    tr.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = "задача"
    tr.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = "язык программирования"
    tr.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = "вердикт"
    tr.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = "время"
    tr.appendChild(cell)
    cell = document.createElement("th")
    cell.innerHTML = "память"
    tr.appendChild(cell)
    header.appendChild(tr)

    let tbody = document.createElement("tbody")
    data.submissions.slice().reverse().forEach(submission => {
        let tr = document.createElement("tr")
        let cell
        cell = document.createElement("td")
        cell.innerHTML = submission.id
        tr.appendChild(cell)
        cell = document.createElement("td")
        cell.innerHTML = (new Date(submission.creation_time_seconds * 1000)).toUTCString()
        tr.appendChild(cell)
        cell = document.createElement("td")
        if (submission.author != null) {
            if (submission.author.hasOwnProperty("team_name")) {
                cell.innerHTML = `команда: ${submission.team.team_name}`
            } else {
                cell.innerHTML = `${submission.author.last_name} ${submission.author.first_name}`
            }
        }
        tr.appendChild(cell)
        cell = document.createElement("td")
        cell.innerHTML = `${submission.problem.contest_id}${submission.problem.index}`
        tr.appendChild(cell)
        cell = document.createElement("td")
        cell.innerHTML = submission.programming_language
        tr.appendChild(cell)
        cell = document.createElement("td")
        cell.innerHTML = submission.verdict
        tr.appendChild(cell)
        cell = document.createElement("td")
        cell.innerHTML = `${submission.time_consumed_millis} мс`
        tr.appendChild(cell)
        cell = document.createElement("td")
        cell.innerHTML = `${submission.memory_consumed_bytes} байт`
        tr.appendChild(cell)

        tbody.appendChild(tr)
    })

    table.appendChild(header)
    table.appendChild(tbody)
    div.appendChild(table)
}
