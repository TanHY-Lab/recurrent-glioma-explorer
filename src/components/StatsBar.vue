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
const sourceCount = computed(() => new Set(props.datasets.map(d => d.source).filter(Boolean)).size)
const omicsCount = computed(() => {
  const types = new Set()
  props.datasets.forEach(d => (d.data_types || []).forEach(t => types.add(t)))
  return types.size
})
const totalSamples = computed(() => props.datasets.reduce((sum, d) => sum + (d.sample_count || 0), 0))
const recurrentSamples = computed(() => props.datasets.reduce((sum, d) => sum + (d.recurrent_sample_count || 0), 0))
</script>

<style scoped>
.stats-bar {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 2px;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(11, 61, 145, 0.4);
  border-radius: 2px;
  overflow: hidden;
}

.stat-card {
  background: #0a1628;
  padding: 1.3rem 1.4rem;
  transition: background 0.2s;
  position: relative;
}

.stat-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: #FC3D21;
  opacity: 0;
  transition: opacity 0.2s;
}

.stat-card:hover::after { opacity: 1; }

.stat-value {
  font-size: 2rem;
  font-weight: 900;
  color: #ffffff;
  letter-spacing: -0.03em;
  margin-bottom: 0.3rem;
  font-variant-numeric: tabular-nums;
}

.stat-label {
  font-size: 0.6rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: #FC3D21;
  font-weight: 700;
}

@media (max-width: 900px) {
  .stats-bar { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 560px) {
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
}
</style>
