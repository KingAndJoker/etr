async function show_contest_table() {
    let response = await fetch("/etr/api/contest")
    let contest_table = document.getElementById("contests-table-body")

    let json = await response.json()
    if (json["status"] != "ok") {
        return
    }

    contests = json["contests"]
    let index = 1
    contests.forEach(contest => {
        let row = contest_table.insertRow()
        let cell = row.insertCell()
        // cell.innerHTML = `${contest["id"]}`
        cell.innerHTML = `${index}`
        index++

        cell = row.insertCell()
        cell.innerHTML = `<a href="/etr/contest/${contest["id"]}">${contest["name"]}</a>`

        let date = new Date(contest["start_time_seconds"] * 1000);
        cell = row.insertCell()
        let month = ["январь",
            "Февраль",
            "Март",
            "Апрель",
            "Май",
            "Июнь",
            "Июль",
            "Август",
            "Сентябрь",
            "Октябрь",
            "Ноябрь",
            "Декабрь"
        ]
        cell.innerHTML = `${month[date.getMonth()]} ${date.getDate()} ${date.getFullYear()}`
    })
}