async function create_table(contest_id) {
    let response = await fetch(`/etr/api/problem/${contest_id}`)
    let problems = await response.json()
    problems = problems["problems"]
    console.log(problems)

    table_acm_result_head = document.getElementById("head_acm_result")
    for (var i = 0; i < problems.length; i++) {
        table_acm_result_head.innerHTML += `<th>${problems[i]["index"]}</th>`
    }

    table_acm_result = document.getElementById("acm_result")

    response = await fetch(`/etr/api/user`)
    let users = await response.json()

    let table_rows = ""
    for (var i = 0; i < users.length; i++) {
        let cells = `<td>${users[i].handle}</td>`

        // TODO: rewrite!!!
        console.log(`https://codeforces.com/api/contest.standings?contestId=${contest_id}&handles=${users[i].handle}`)
        let codeforces_response_user_rows = await fetch(`https://codeforces.com/api/contest.standings?contestId=${contest_id}&handles=${users[i].handle}`)
        let codeforces_json_user_rows = await codeforces_response_user_rows.json()

        for (var j = 0; j < problems.length; j++) {
            let attempt_cell = ""
            let scores_cell = ""
            let cell = ""

            let cell_response = await fetch(`/etr/api/submission?handle=${users[i]["handle"]}&contest_id=${contest_id}&problem_index=${problems[j]["index"]}`)
            let cell_status = await cell_response.json()

            if (cell_status.length > 0) {
                attempt_cell = cell_status.length
                scores_cell = ""

                let complete = false
                let maxScore = null
                for (var k = 0; k < cell_status.length && !complete; k++) {
                    if (cell_status[k]["verdict"] === "OK") {
                        complete = true

                        // TODO: rewrite
                        if (codeforces_json_user_rows["result"]["rows"].length > 0) {
                            if (codeforces_json_user_rows["result"]["rows"][0]["problemResults"][j]["points"] != 0) {
                                maxScore = codeforces_json_user_rows["result"]["rows"][0]["problemResults"][j]["points"]
                            } else {
                                maxScore = problems[j].points
                            }
                        }
                    }
                }
                // TODO: was the solution sent during the contest?
                scores_cell = `${maxScore}`
                cell = ""
                if (complete) {
                    attempt_cell = `<p class="attempt_cell">+${attempt_cell}</p>`
                    scores_cell = `<p class="none">${scores_cell}</p>`
                    cell = `<div class="successfully">${attempt_cell}${scores_cell}</div>`
                }
                else {
                    attempt_cell = `<p class="attempt_cell">-${attempt_cell}</p>`
                    scores_cell = `<p class="none">${attempt_cell}</p>`
                    cell = `<div class="fail">${attempt_cell}${scores_cell}</div>`
                }
            }

            cells += `<td>${cell}</td>`
        }

        table_rows += `<tr>${cells}</tr>`
    }
    table_acm_result.innerHTML += table_rows
}