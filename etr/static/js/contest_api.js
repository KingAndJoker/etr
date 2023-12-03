let type_of_contests = null


async function show_contest_table() {
    let response = await fetch("/etr/api/contest")
    let contest_table = document.getElementById("contests-table-body")
    contest_table.innerHTML = ""

    let json = await response.json()
    if (json["status"] != "ok") {
        return
    }

    contests = json["contests"]
    let index = 1
    contests.forEach(async (contest) => {
        if (type_of_contests == "all" || type_of_contests == contest.type_of_source) {
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
        }
    })
}


const get_type_of_contests = () => {
    let url = new URL(window.location.href)
    let type_sub = url.searchParams.get("type_contests")
    if (type_sub == null) {
        type_sub = "all"
    }
    set_checkboxes_type_of_contests(type_sub)
    return type_sub
}

const set_checkboxes_type_of_contests = (type_contests) => {
    let radiobtn = document.getElementById(`${type_contests}_type_of_contests`)
    radiobtn.checked = true;
}

const change_type_of_contests = () => {
    const radioButtons = document.querySelectorAll("input[name=type_of_contests]")

    for (const radioButton of radioButtons) {
        radioButton.addEventListener('change', show_selected_contests)
    }
}

const show_selected_contests = (event) => {
    let url = new URL(window.location.href)
    url.searchParams.set('type_contests', `${event.target.value}`)
    window.history.replaceState(null, null, url)

    type_of_contests = event.target.value
    show_contest_table()
}