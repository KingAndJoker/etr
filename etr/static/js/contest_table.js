function create_table_head(data) {
    let thead = document.createElement("thead")
    let tr = document.createElement("tr")
    tr.id = "head_acm_result"
    tr.classList = "table-dark"
    let th = document.createElement("th")
    th.innerText = "#"
    tr.appendChild(th)
    th = document.createElement("th")
    th.innerText = "ученик"
    tr.appendChild(th)

    for (var i = 0; i < data.contest.problems.length; i++) {
        th = document.createElement("th")
        th.innerText = data.contest.problems[i].index
        tr.appendChild(th)
    }
    thead.appendChild(tr)
    return thead
}


function get_handles(data) {
    handles = data.rows.map(row => row.user.handle)
    return handles
}


async function create_table_body(data, contest_id) {
    let tbody = document.createElement("tbody")

    handles = get_handles(data).join(";")
    let cf_response = await fetch(`https://codeforces.com/api/contest.standings?contestId=${contest_id}&handles=${handles}&showUnofficial=True`)
    let cf_data = null
    if (cf_response.status == 200) {
        cf_data = await cf_response.json()
    }

    let index = 1
    data.rows.forEach(row => {
        let tr = document.createElement("tr")

        let th = document.createElement("th")
        th.innerText = `${index}`
        tr.appendChild(th)
        index++

        let td = document.createElement("td")
        let user_name = `${row.user.last_name} ${row.user.first_name}, ${row.user.organization}`
        if (row.user.grade) {
            user_name = `${user_name}, ${row.user.grade} класс`
        }
        td.innerHTML = user_name
        tr.appendChild(td)

        let task_result = {}
        for (var i = 0; i < data.contest.problems.length; i++) {
            task_result[data.contest.problems[i].index] = {
                count: 0,
                solved: false,
                max_point: 0,
            }
        }

        row.submissions.forEach(submission => {
            task_result[submission.problem.index].count++
            if (submission.verdict == "OK") {
                task_result[submission.problem.index].solved = true
            }
            if (task_result[submission.problem.index].max_point < submission.points) {
                task_result[submission.problem.index].max_point = submission.points
            }
            if (cf_data) {
                try {
                    let cf_row = cf_data.result.rows.find(cf_row => cf_row.party.members[0].handle == row.user.handle)
                    let cf_problem_index = 0
                    while (data.contest.problems[cf_problem_index].index != submission.problem.index) {
                        cf_problem_index++
                    }
                    if (cf_row.problemResults[cf_problem_index].points && task_result[submission.problem.index].max_point < cf_row.problemResults[cf_problem_index].points) {
                        task_result[submission.problem.index].max_point = cf_row.problemResults[cf_problem_index].points
                    }
                }
                catch {}
            }
        })

        for (var i = 0; i < data.contest.problems.length; i++) {
            let td = document.createElement("td")
            let problem_index = data.contest.problems[i].index

            if (task_result[problem_index].count) {
                if (task_result[problem_index].solved) {
                    let attempt_cell = `<p class="attempt_cell">+${task_result[problem_index].count}</p>`
                    let scores_cell = `<p class="none">${task_result[problem_index].max_point}</p>`
                    let cell = `<div class="successfully">${attempt_cell}${scores_cell}</div>`
                    td.innerHTML = cell
                }
                else {
                    let attempt_cell = `<p class="attempt_cell">-${task_result[problem_index].count}</p>`
                    let scores_cell = `<p class="none">${0}</p>`
                    let cell = `<div class="fail">${attempt_cell}${scores_cell}</div>`
                    td.innerHTML = cell
                }
            }
            tr.appendChild(td)
        }

        tbody.appendChild(tr)
    })

    return tbody
}


async function create_table(contest_id) {
    let div_table = document.getElementById("div-contest-table")
    let table = document.createElement("table")
    table.classList = "table table-striped table-hover table-bordered w-auto"
    table.id = "acm_result"

    let response = await fetch(`/etr/api/contest/${contest_id}/table`)
    if (!response.ok) {
        return
    }
    let data = await response.json()

    table.appendChild(create_table_head(data))

    table.appendChild(await create_table_body(data, contest_id))

    div_table.appendChild(table)
}