async function send_request_sync_user_with_dl() {
    let response = await fetch("/etr/rpc/user/swdl")
    let json = await response.json()

    show_table()

    return json["status"]
}


async function create_users_table() {
    let users_table = document.getElementById("users-table")
    if (users_table === null) {
        return
    }

    let response = await fetch("/etr/api/user/")
    let response_json = await response.json()
    if (response_json["status"] != "ok") {
        return
    }

    users = response_json["users"]

    while (users_table.rows.length > 0) {
        users_table.deleteRow(0)
    }

    let table_header = users_table.createTHead()
    table_header.classList = "table-dark"
    let head_row = table_header.insertRow()
    let head = get_header()

    // head.forEach(element => {
    //     let cell = head_row.insertCell().outerHTML = `<th>${element}</th>`
    // });
    head_row.insertCell().outerHTML = `<th>handle</th>`
    head_row.insertCell().outerHTML = `<th>фамилия</th>`
    head_row.insertCell().outerHTML = `<th>имя</th>`
    head_row.insertCell().outerHTML = `<th>организация</th>`
    head_row.insertCell().outerHTML = `<th>город</th>`
    head_row.insertCell().outerHTML = `<th>класс</th>`


    let table_body = users_table.createTBody()
    users.forEach(user => {
        let row = table_body.insertRow()
        head.forEach(element => {
            let cell = row.insertCell()
            if (user[element]) {
                cell.innerHTML = `${user[element]}`
            }
        });
    })
}


function get_header() {
    return [
        "handle",
        "last_name",
        "first_name",
        "organization",
        "city",
        "grade",
    ]
}


async function init_table() {
    let content = document.getElementById("user-table-div")
    let users_table = document.createElement("table")
    users_table.id = "users-table"
    users_table.classList = "table table-striped table-hover table-bordered"

    content.append(users_table)

    return users_table
}


async function show_table() {
    let users_table = document.getElementById("users-table")

    if (users_table === null) {
        users_table = init_table()
    }

    create_users_table()
}


async function send_request_sync_user_with_codeforces() {
    let response = await fetch("/etr/api/user")
    if (!response.ok) {
        return
    }
    let users = await response.json()

    for(var i=0; i<users.users.length; i++) {
        let response_user_update = await fetch(`/etr/api/user/update_codeforces/${users.users[i].handle}`)
        console.log(`update codeforces: /etr/api/user/update_codeforces/${users.users[i].handle}; status: ${response_user_update.ok}`)``
    }
}
