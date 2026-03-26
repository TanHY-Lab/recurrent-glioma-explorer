<template>
  <div class="explorer-page">
    <!-- Page Header -->
    <header class="page-header">
      <div class="header-inner">
        <div class="header-left">
          <a href="./index.html" class="back-link">&larr; Home</a>
          <h1>Recurrent Glioma <span class="accent">Multi-Omics</span> Explorer</h1>
          <p class="header-sub">复发胶质瘤多组学数据浏览器 &mdash; Integrated dataset explorer for recurrent glioma research</p>
        </div>
      </div>
    </header>

    <!-- Stats -->
    <div class="content-area">
      <StatsBar :datasets="filteredDatasets" :all-datasets="datasets" />

      <!-- Filters -->
      <FilterPanel
        :datasets="datasets"
        :initial-source="initialSource"
        :initial-type="initialType"
        @filter-change="onFilterChange"
      />

      <!-- Table -->
      <DataTable :datasets="filteredDatasets" :loading="loading" />
    </div>

    <!-- Footer -->
    <footer class="site-footer">
      <p>Recurrent Glioma Multi-Omics Explorer &middot; Data aggregated from GEO, GLASS, CGGA, TCGA, CPTAC, cBioPortal and other sources</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import StatsBar from '../components/StatsBar.vue'
import FilterPanel from '../components/FilterPanel.vue'
import DataTable from '../components/DataTable.vue'

const props = defineProps({
  datasets: { type: Array, default: () => [] },
  loading: { type: Boolean, default: true },
  initialSource: { type: String, default: '' },
  initialType: { type: String, default: '' }
})

const filters = ref({
  keyword: '',
  sources: [],
  dataTypes: [],
  subtypes: [],
  pairedOnly: false
})

function onFilterChange(newFilters) {
  filters.value = { ...newFilters }
}

const filteredDatasets = computed(() => {
  let result = props.datasets

  const { keyword, sources, dataTypes, subtypes, pairedOnly } = filters.value

  if (keyword) {
    const kw = keyword.toLowerCase()
    result = result.filter(d =>
      (d.title || '').toLowerCase().includes(kw) ||
      (d.accession || '').toLowerCase().includes(kw) ||
      (d.summary || '').toLowerCase().includes(kw) ||
      (d.contributors || '').toLowerCase().includes(kw) ||
      (d.institution || '').toLowerCase().includes(kw)
    )
  }

  if (sources.length > 0) {
    result = result.filter(d => sources.includes(d.source))
  }

  if (dataTypes.length > 0) {
    result = result.filter(d => {
      const dt = d.data_types || []
      return dataTypes.some(t => dt.includes(t))
    })
  }

  if (subtypes.length > 0) {
    result = result.filter(d => {
      const st = d.tumor_subtypes || []
      return subtypes.some(t => st.includes(t))
    })
  }

  if (pairedOnly) {
    result = result.filter(d => (d.recurrent_sample_count || 0) > 0)
  }

  return result
})
</script>

<style scoped>
.explorer-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.page-header {
  background: linear-gradient(135deg, #0a0e27 0%, #0f1535 40%, #131a3e 100%);
  border-bottom: 1px solid rgba(0, 212, 170, 0.1);
  padding: 2rem 2.5rem;
  position: relative;
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 212, 170, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 212, 170, 0.04) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
}

.header-inner {
  position: relative;
  z-index: 1;
  max-width: 1400px;
  margin: 0 auto;
}

.back-link {
  display: inline-block;
  color: #8892b0;
  text-decoration: none;
  font-size: 0.8rem;
  margin-bottom: 0.8rem;
  letter-spacing: 0.03em;
  transition: color 0.2s;
}

.back-link:hover { color: #00d4aa; }

.page-header h1 {
  font-size: 1.6rem;
  font-weight: 500;
  color: #ffffff;
  letter-spacing: 0.01em;
  margin-bottom: 0.4rem;
}

.accent { color: #00d4aa; }

.header-sub {
  color: #8892b0;
  font-size: 0.85rem;
  font-weight: 300;
  letter-spacing: 0.02em;
}

.content-area {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 1.5rem 2.5rem 2rem;
}

.site-footer {
  text-align: center;
  padding: 1.5rem;
  color: #4a5580;
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  border-top: 1px solid rgba(0, 212, 170, 0.06);
}

@media (max-width: 768px) {
  .page-header { padding: 1.5rem 1rem; }
  .content-area { padding: 1rem; }
  .page-header h1 { font-size: 1.2rem; }
}
</style>
