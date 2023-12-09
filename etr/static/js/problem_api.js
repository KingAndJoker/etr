const create_table = async () => {
    let table = document.getElementById("problems-table")
    let response = await fetch("/etr/api/problem")
    if (!response.ok) {
        table.innerHTML = "<h1>Возникла проблема, попробуй позже.</h1>"
        return
    }
    let data = await response.json()
    problems = data.problems

    table = document.getElementById("problems-table-tbody")
    problems.forEach((problem) => {
        let row = table.insertRow()
        let cell
        cell = row.insertCell()
        cell.innerHTML = `${problem.id}`

        cell = row.insertCell()
        cell.innerHTML = `${problem.contest_id}`

        cell = row.insertCell()
        cell.innerHTML = `${problem.index}`

        cell = row.insertCell()
        cell.innerHTML = `${problem.name}`

        cell = row.insertCell()
        cell.innerHTML = `${problem.points != null ? problem.points : ""}`

        cell = row.insertCell()
        cell.innerHTML = `${problem.rating != null ? problem.rating : ""}`
    })
}
