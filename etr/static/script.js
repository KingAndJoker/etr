let status = 1

function switch_view_cell() {
    if (status) {
        status = 0
        let cells = document.getElementsByClassName("none")
        while (cells.length > 0) {
            cells[0].className = "score_cell"
        }

        cells = document.getElementsByClassName("attempt_cell")
        while (cells.length > 0) {
            cells[0].className = "none"
        }
    }
    else {
        status = 1
        let cells = document.getElementsByClassName("none")
        while (cells.length > 0) {
            cells[0].className = "attempt_cell"
        }

        cells = document.getElementsByClassName("score_cell")
        while (cells.length > 0) {
            cells[0].className = "none"
        }
    }
}


async function update_submission_send_request(contest_id) {
    let response = await fetch(`/etr/api/user`)
    let users = await response.json()

    response = await fetch(`/etr/api/problem/${contest_id}`)
    let problems = await response.json()
    problems = problems["problems"]

    for (var i = 0; i < users.length; i++) {
        let url = `/etr/rpc/submission/${contest_id}?handle=${users[i].handle}`
        console.log(url)
        response = await fetch(url)
    }

    window.location.reload()
}
