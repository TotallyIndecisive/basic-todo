<script setup>
import { ref, onMounted } from 'vue'

import {
  getTodos,
  createTodo,
  deleteTodo,
  deleteTodos
} from './services/api'

const todos = ref([])
const title = ref('')
const selected = ref(new Set())

async function loadTodos() {
  todos.value = await getTodos()
}

async function addTodo() {

  if (!title.value.trim()) return

  await createTodo(title.value)

  title.value = ''

  await loadTodos()
}

async function removeTodo(id) {
  await deleteTodo(id)
  selected.value.delete(id)
  await loadTodos()
}

async function removeSelected() {
  const ids = [...selected.value]
  if (!ids.length) return
  await deleteTodos(ids)
  selected.value = new Set()
  await loadTodos()
}

function toggle(id) {
  const s = new Set(selected.value)
  s.has(id) ? s.delete(id) : s.add(id)
  selected.value = s
}

function toggleAll() {
  if (selected.value.size === todos.value.length) {
    selected.value = new Set()
  } else {
    selected.value = new Set(todos.value.map(t => t.id))
  }
}

onMounted(loadTodos)
</script>

<template>

<div class="max-w-lg mx-auto mt-10">

  <h1 class="text-3xl font-bold mb-4">
    Todo App
  </h1>

  <div class="flex gap-2 mb-4">

    <input
      v-model="title"
      class="border p-2 flex-1"
      placeholder="Enter task"
    />

    <button
      @click="addTodo"
      class="bg-black text-white px-4 py-2"
    >
      Add
    </button>

  </div>

  <div class="flex gap-2 mb-4">

    <button
      @click="toggleAll"
      class="border px-3 py-1 text-sm"
    >
      {{ selected.size === todos.length ? "Deselect All" : "Select All" }}
    </button>

    <button
      @click="removeSelected"
      :disabled="!selected.size"
      class="bg-red-600 text-white px-3 py-1 text-sm disabled:opacity-40"
    >
      Delete Selected ({{ selected.size }})
    </button>

  </div>

  <ul>

    <li
      v-for="todo in todos"
      :key="todo.id"
      class="flex items-center gap-2 border p-2 mb-2"
    >

      <input
        type="checkbox"
        :checked="selected.has(todo.id)"
        @change="toggle(todo.id)"
        class="shrink-0"
      />

      <span class="flex-1">{{ todo.title }}</span>

      <button
        @click="removeTodo(todo.id)"
        class="text-red-600 text-sm hover:underline"
      >
        Delete
      </button>

    </li>

  </ul>

</div>

</template>