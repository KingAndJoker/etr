const create_table = async () => {
    const urlParams = new URLSearchParams(window.location.search)
    const rating = urlParams.get('rating')
    let table = document.getElementById("problems-table")
    let url = "/etr/api/problem?"
    if (rating != null) {
        url += `rating=${rating}`
    }
    let response = await fetch(url)
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

        cell = row.insertCell()
        cell.innerHTML = `${problem.solved_count != null ? problem.solved_count : ""}`
    })
}
