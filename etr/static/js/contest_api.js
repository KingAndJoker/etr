async function show_contest_table() {
    let response = await fetch("/etr/api/contest")
    let contest_table = document.getElementById("contests-table-body")

    let json = await response.json()
    if (json["status"] != "ok") {
        return
    }

    contests = json["contests"]
    let index = 1
    contests.forEach(async (contest) => {
        let row = contest_table.insertRow()
        let cell = row.insertCell()
        cell.innerHTML = `${index}`
        index++

        cell = row.insertCell()
        cell.innerHTML = `<a href="/etr/contest/${contest["id"]}">${contest["name"]}</a>`

        let date = new Date(contest["start_time_seconds"] * 1000);
        cell = row.insertCell()
        let month = [
            "январь",
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

        cell = row.insertCell()
        const show_count_of_participant = async (cell) => {
            let table_contest_response = await fetch(`/etr/api/contest/${contest["id"]}/table`)
            if (table_contest_response.ok) {
                let table_contest = await table_contest_response.json()
                cell.innerHTML = `${table_contest.rows.length}`
            } else {
                cell.innerHTML = `error`
            }
        }
        show_count_of_participant(cell)

        cell = row.insertCell()
        cell.innerHTML = `
            <a href="/etr/contest/${contest.id}?type_sub=contest">контест</a>
            <a href="/etr/contest/${contest.id}?type_sub=virtual">виртуально</a>
        `
    })
}