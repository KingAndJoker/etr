const send_update_users_submissions = async (handle) => {
    let response = await fetch(`/etr/rpc/submission/user/${handle}`)
    if (response.ok) {
        alert("пользователь обновляется")
    }
    else {
        alert("произошла ошибка, попробуйте повторить запрос позже")
    }
}

const send_request_update_all_submissions_for_all_users = async () => {
    let response = await fetch(`/etr/rpc/submissions/users`)
    if (response.ok) {
        alert("пользователи обновляются")
    }
    else {
        alert("произошла ошибка, попробуйте повторить запрос позже")
    }
}