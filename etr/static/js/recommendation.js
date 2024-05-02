const render_recommendations = async () => {
    let div_recommendations = document.getElementById("div-recommendations")
    div_recommendations.innerHTML = ""

    let handle = document.getElementById("handle-input").value
    let response = await fetch(`/etr/api/recommendation/${handle}`)

    if (!response.ok) {
        div_recommendations.innerHTML = "<h1>Попробуйте позже...</h1>"
        return
    }

    let data = await response.json()

    let about_user = document.createElement("div")
    let user = data.user
    about_user.className = "container"
    about_user.innerHTML = `
    <h2>Рекомендации для ${user.first_name} ${user.last_name}</h2><br>
    `


    let table = document.createElement("table")
    table.classList = "table table-striped table-hover table-responsive"

    let thead = document.createElement("thead")
    thead.className = "table-dark"
    let tbody = document.createElement("tbody")

    let row
    row = document.createElement("tr")
    let cell
    cell = document.createElement("td")
    cell.innerHTML = "задача"
    row.appendChild(cell)
    cell = document.createElement("td")
    cell.innerHTML = "название"
    row.appendChild(cell)
    cell = document.createElement("td")
    cell.innerHTML = "сложность"
    row.appendChild(cell)
    cell = document.createElement("td")
    cell.innerHTML = "теги"
    row.appendChild(cell)
    cell = document.createElement("td")
    cell.innerHTML = "количество решивших"
    row.appendChild(cell)

    thead.appendChild(row)

    data.recommendations.map((recommendation) => {
        let row = document.createElement("tr")
        let cell
        cell = document.createElement("td")
        if (recommendation.problem.contest_id < 100000) {
            cell.innerHTML = `<a href="http://codeforces.com/problemset/problem/${recommendation.problem.contest_id}/${recommendation.problem.index}">${recommendation.problem.contest_id}${recommendation.problem.index}</a>`
        }
        else {
            cell.innerHTML = `<a href="http://codeforces.com/gym/${recommendation.problem.contest_id}/problem/${recommendation.problem.index}">${recommendation.problem.contest_id}${recommendation.problem.index}</a>`
        }
        row.appendChild(cell)
        
        cell = document.createElement("td")
        cell.innerHTML = `${recommendation.problem.name}`
        row.appendChild(cell)

        cell = document.createElement("td")
        cell.innerHTML = `${recommendation.problem.rating ? recommendation.problem.rating : "-"}`
        row.appendChild(cell)

        cell = document.createElement("td")
        cell.innerHTML = recommendation.problem.tags.map((tag) => {
            return `<mark class="border" style="margin: 5px">${tag}</mark>`
        }).join("")
        row.appendChild(cell)

        cell = document.createElement("td")
        cell.innerHTML = `${recommendation.problem.solved_count}`
        row.appendChild(cell)

        return row
    }).forEach(element => {
        tbody.append(element)
    })

    table.appendChild(thead)
    table.appendChild(tbody)

    div_recommendations.appendChild(about_user)
    div_recommendations.appendChild(table)
}