<template>
  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-value">{{ datasetCount }}</div>
      <div class="stat-label">{{ t('statDatasets') }}</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ sourceCount }}</div>
      <div class="stat-label">{{ t('statSources') }}</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ omicsCount }}</div>
      <div class="stat-label">{{ t('statOmics') }}</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ totalSamples.toLocaleString() }}</div>
      <div class="stat-label">{{ t('statSamples') }}</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{{ recurrentSamples.toLocaleString() }}</div>
      <div class="stat-label">{{ t('statRecurrent') }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { t } from '../i18n.js'

const props = defineProps({
  datasets: { type: Array, default: () => [] },
  allDatasets: { type: Array, default: () => [] }
})

const datasetCount = computed(() => props.datasets.length)

const sourceCount = computed(() => {
  const sources = new Set(props.datasets.map(d => d.source).filter(Boolean))
  return sources.size
})

const omicsCount = computed(() => {
  const types = new Set()
  props.datasets.forEach(d => {
    (d.data_types || []).forEach(t => types.add(t))
  })
  return types.size
})

const totalSamples = computed(() => {
  return props.datasets.reduce((sum, d) => sum + (d.sample_count || 0), 0)
})

const recurrentSamples = computed(() => {
  return props.datasets.reduce((sum, d) => sum + (d.recurrent_sample_count || 0), 0)
})
</script>

<style scoped>
.stats-bar {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: #131a3e;
  border: 1px solid rgba(0, 212, 170, 0.1);
  border-radius: 6px;
  padding: 1.2rem 1.4rem;
  transition: border-color 0.2s;
}

.stat-card:hover {
  border-color: rgba(0, 212, 170, 0.3);
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #00d4aa;
  letter-spacing: -0.02em;
  margin-bottom: 0.3rem;
}

.stat-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #8892b0;
  font-weight: 500;
}

@media (max-width: 900px) {
  .stats-bar { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 560px) {
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
}
</style>
