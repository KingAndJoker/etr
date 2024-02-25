const send_update_users_submissions = async (handle) => {
    let response = await fetch(`/etr/rpc/submission/user/${handle}`)
    if (response.ok) {
        alert("пользователь обновляется")
    }
    else {
        alert("произошла ошибка, попробуйте повторить запрос позже")
    }
}