<template>
  <Explorer :datasets="datasets" :loading="loading" :initial-source="initialSource" :initial-type="initialType" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Explorer from './views/Explorer.vue'

const datasets = ref([])
const loading = ref(true)
const initialSource = ref('')
const initialType = ref('')

onMounted(async () => {
  const params = new URLSearchParams(window.location.search)
  initialSource.value = params.get('source') || ''
  initialType.value = params.get('type') || ''

  try {
    const url = `./data/datasets.json?ts=${Date.now()}`
    const response = await fetch(url, { cache: 'no-store' })
    if (response.ok) {
      datasets.value = await response.json()
    } else {
      console.warn('Failed to load datasets.json, status:', response.status)
      datasets.value = []
    }
  } catch (err) {
    console.error('Error loading datasets:', err)
    datasets.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
}
</style>
