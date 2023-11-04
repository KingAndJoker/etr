async function show_contest_table() {
    let response = await fetch("/etr/api/contest")
    let contest_table = document.getElementById("contests-table-body")

    let json = await response.json()
    if (json["status"] != "ok") {
        return
    }

    contests = json["contests"]
    contests.forEach(contest => {
        let row = contest_table.insertRow()
        let cell = row.insertCell()
        cell.innerHTML = `${contest["id"]}`

        cell = row.insertCell()
        cell.innerHTML = `<a href="/etr/contest/${contest["id"]}">${contest["name"]}</a>}`

        cell = row.insertCell()
        cell.innerHTML = `${contest["type"]}`

        cell = row.insertCell()
        cell.innerHTML = `${contest["phase"]}`

        cell = row.insertCell()
        cell.innerHTML = `${contest["frozen"]}`

        let date = new Date(contest["start_time_seconds"] * 1000);
        cell = row.insertCell()
        cell.innerHTML = `${date}`
    })
}