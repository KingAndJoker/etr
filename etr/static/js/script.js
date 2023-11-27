const get_type_of_view = () => {
    let url = new URL(window.location.href)
    let type = url.searchParams.get("view_point")
    if (type == null) {
        type = "1"
    }
    type = parseInt(type)

    return type
}


const show_selected_type_of_view = () => {
    let url = new URL(window.location.href)
    url.searchParams.set('view_point', `${type_of_view_points}`)
    window.history.replaceState(null, null, url)
}


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
    show_selected_type_of_view()
}


async function update_submission_send_request(contest_id) {
    let url = `/etr/rpc/submission/${contest_id}`
    console.log(url)
    let response = await fetch(url)

    window.location.reload()
}
