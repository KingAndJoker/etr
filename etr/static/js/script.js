let type_of_view_points = 1

async function switch_view_cell() {
    if (type_of_view_points) {
        type_of_view_points = 0
        await show_table()
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
        type_of_view_points = 1
        await show_table()
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
    let url = `/etr/rpc/submission/${contest_id}`
    console.log(url)
    let response = await fetch(url)

    window.location.reload()
}
