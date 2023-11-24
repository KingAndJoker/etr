var type_of_submisions = null
var contest_id = 0
var codeforces_data = null
var etr_data = null


async function get_etr_data() {
    let data = await fetch(`/etr/api/contest/${contest_id}/table`)
    etr_data = await data.json()
    return etr_data
}


const get_handles = () => {
    handles = []
    etr_data.rows.forEach(row => {
        if (row.user != undefined) {
            if (!handles.includes(row.user.handle)) {
                handles.push(row.user.handle)
            }
        }
        if (row.team != undefined) {
            row.team.users.forEach(user => {
                if (!handles.includes(user.handle)) {
                    handles.push(user.handle)
                }
            })
        }
    })

    handles = handles.filter((item) => item != null && item != undefined)

    return handles
}


async function get_codeforces_data() {
    get_etr_data()
    if (codeforces_data == null) {
        let data = await fetch(`https://codeforces.com/api/contest.standings?contestId=${contest_id}&showUnofficial=true&handles=${get_handles().join(";")}`)
        try {
            codeforces_data = await data.json()
        }
        catch {
            codeforces_data = null
        }
    }
    return codeforces_data
}


function set_checkboxes_type_of_submissions(type_sub) {
    let radiobtn = document.getElementById(`${type_sub}_type_of_submissions`)
    radiobtn.checked = true;
}


function get_type_of_submissions() {
    let url = new URL(window.location.href)
    let type_sub = url.searchParams.get("type_sub")
    if (type_sub == null) {
        type_sub = "all"
    }
    set_checkboxes_type_of_submissions(type_sub)
    return type_sub
}


function get_thead(problems) {
    return `
    <thead class="table-dark">
        <tr id="head_acm_result">
            <th scope="col">#</th>
            <th scope="col">участник</th>
            <th scope="col">город</th>
            <th scope="col">организация</th>
            <th scope="col">класс</th>
            <th scope="col">${type_of_view_points == 1 ? "задачи" : "баллы"}</th>
            ${problems.map(problem => `<th scope="col">${problem.index}</th>`).join("")}
        </tr>
    </thead>
    `
}


const get_author = (row) => {
    if (row.user != undefined) {
        return `${row.user.first_name} ${row.user.last_name}`
    }
    if (row.team != undefined) {
        return `<b>${row.team.team_name}</b><br>${row.team.users.map(user => user.handle).join(", ")}`
    }
}


const get_problems_row = (problems) => {
    return problems.map((problem) => {
        if (problem.score) {
            if (problem.status) {
                if (type_of_view_points) {
                    return `<td><div class="successfully">${type_of_view_points ? "+" : ""}${problem.score > 1 ? problem.score : ""}</div></td>`
                }
                else {
                    return `<td><div class="successfully">${problem.score}</div></td>`
                }
            }
            else {
                return `<td><div class="fail">-${problem.score}</div></td>`
            }
        }
        return `<td></td>`
    }).join("")
}


const create_row = (id, author, city, organization, grade, points, problems) => {
    let tr = `<tr>
            <th scope="row">${id}</th>
            <td>${author}</td>
            <td>${city}</td>
            <td>${organization}</td>
            <td>${grade}</td>
            <td>${points}</td>
            ${get_problems_row(problems)}
        </tr>
    `
    return tr
}


function get_value_from_dict(obj, keys, default_value) {
    let key = keys.split(".")[0]
    if (obj[key] == undefined) {
        return default_value
    }
    else {
        let k = keys.split(".")
        k.pop()
        return get_value_from_dict(obj, k.join("."), default_value)
    }
}


const get_points_from_codeforces = (handle, index) => {
    ind = codeforces_data.result.problems.findIndex((problem) => {
        return problem.index == index
    })
    if (codeforces_data == null) {
        return 1
    }
    let row = codeforces_data.result.rows.find((row) => {
        return row.party.members[0].handle == handle
    })
    if (row == undefined) {
        return 1
    }
    let problem = row.problemResults[ind]
    if (problem == undefined) {
        return 1
    }
    return problem.points
}


const create_table = (contest, rows) => {
    let table = ``

    let thead = get_thead(contest.problems)
    let tbody = rows.map((row) => {
        let table_row = {
            id: 1,
            author: get_author(row),
            city: get_value_from_dict(row, "user.city", "-"),
            organization: get_value_from_dict(row, "user.organization", "-"),
            grade: get_value_from_dict(row, "user.grade", "-"),
            score: 0,
            problems: contest.problems.map((problem) => ({ score: 0, status: 0, index: problem.index }))
        }

        row.submissions.forEach((submission) => {
            if (submission.verdict == "OK") {
                if (type_of_view_points) {
                    table_row.problems = table_row.problems.map((problem) => {
                        if (problem.index == submission.problem.index) {
                            if (problem.status == 0) {
                                table_row.score++
                            }
                            problem.status = 1
                            problem.score++
                        }
                        return problem
                    })
                } else {
                    table_row.problems = table_row.problems.map((problem) => {
                        if (problem.index != submission.problem.index) {
                            return problem
                        }
                        if (type_of_submisions == "contest" || type_of_submisions == "virtual") {
                            if (row.user != undefined) {
                                problem.score = get_points_from_codeforces(row.user.handle, submission.problem.index)
                                table_row.score += problem.score
                            }
                            else {
                                problem.score = get_points_from_codeforces_team(row.team.team_name, submission.problem.index)
                                table_row.score += problem.score
                            }
                        }
                        else {
                            problem.score = submission.problem.points == null ? 1 : submission.problem.points
                            table_row.score += problem.score
                        }
                        problem.status = 1
                        return problem
                    })
                }
            } else {
                table_row.problems = table_row.problems.map((problem) => {
                    if (problem.index == submission.problem.index) {
                        problem.score++
                    }
                    return problem
                })
            }
        })

        return table_row
    })

    tbody.sort((a, b) => a.score < b.score)
    let id = 1
    tbody = tbody.map((row) => {
        row.id = id
        id++
        return create_row(row.id, row.author, row.city, row.organization, row.grade, row.score, row.problems)
    }).join("")

    table = `<table id="acm_result" class="table table-striped table-hover table-bordered w-auto">
    ${thead}
    ${tbody}
    </table>`

    return table
}


const correct_submissions_list = ({ submissions }, types_of_sub) => {
    return submissions.filter((submission) => {
        return types_of_sub.includes(submission.type_of_member)
    })
}


const all_submissions_rows = ({ rows }) => {
    return rows
}


const contest_submissions_rows = ({ rows }) => {
    rows.forEach((row) => {
        row.submissions = row.submissions.filter((submission) => {
            return submission.type_of_member == "CONTESTANT"
        })
    })
    return rows
}

function virtual_submissions_rows({ rows }) {
    return rows.map((row) => {
        row.submissions = row.submissions.filter((submission) => {
            return submission.type_of_member == "VIRTUAL"
        })
        return row
    })
}

function other_submissions_rows({ rows }) {
    return rows.map((row) => {
        row.submissions = row.submissions.filter((submission) => {
            return (submission.type_of_member == "MANAGER" || submission.type_of_member == "OUT_OF_COMPETITION" || submission.type_of_member == "PRACTICE")
        })
        return row
    })
}

async function show_table() {
    let rows = []
    etr_data = await get_etr_data()
    let contest = etr_data.contest

    if (type_of_submisions == "all") {
        rows = all_submissions_rows(etr_data)
    }
    if (type_of_submisions == "contest") {
        rows = contest_submissions_rows(etr_data)
    }
    if (type_of_submisions == "virtual") {
        rows = virtual_submissions_rows(etr_data)
    }
    if (type_of_submisions == "other") {
        rows = other_submissions_rows(etr_data)
    }

    document.getElementById("div-contest-table").innerHTML = create_table(contest, rows)
}

async function setting_table() {
    await get_etr_data()
    await get_codeforces_data()
    change_type_of_submissions()
}

function change_type_of_submissions() {
    const radioButtons = document.querySelectorAll("input[name=type_of_submissions]")

    for (const radioButton of radioButtons) {
        radioButton.addEventListener('change', show_selected)
    }
}

function show_selected(event) {
    let url = new URL(window.location.href)
    url.searchParams.set('type_sub', `${event.target.value}`)
    window.history.replaceState(null, null, url)

    type_of_submisions = event.target.value
    show_table()
}

async function start() {
    await setting_table()
    await show_table()
}
