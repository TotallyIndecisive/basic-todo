const API_URL =
  import.meta.env.VITE_API_URL

export async function getTodos() {

  const response = await fetch(
    `${API_URL}/todos/`
  )

  return response.json()
}

export async function createTodo(title) {

  const response = await fetch(
    `${API_URL}/todos/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        title
      })
    }
  )

  return response.json()
}

export async function deleteTodo(id) {

  await fetch(`${API_URL}/todos/${id}`, {
    method: "DELETE"
  })
}

export async function deleteTodos(ids) {

  await fetch(`${API_URL}/todos/`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ ids })
  })
}