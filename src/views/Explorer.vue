<template>
  <div class="explorer-page">
    <!-- Page Header with BG image -->
    <header class="page-header">
      <div class="header-bg"></div>
      <div class="header-overlay"></div>
      <div class="header-inner">
        <div class="header-top-row">
          <a href="./index.html" class="back-link">&larr; {{ t('backHome') }}</a>
          <LangSwitcher />
        </div>
        <div class="header-badge">RG-OMICS</div>
        <h1>{{ t('explorerTitle') }} <span class="accent">{{ t('explorerTitleAccent') }}</span> {{ t('explorerTitleEnd') }}</h1>
        <p class="header-sub">{{ t('explorerSubtitle') }}</p>
      </div>
    </header>

    <!-- Stats -->
    <div class="content-area">
      <StatsBar :datasets="filteredDatasets" :all-datasets="datasets" />
      <FilterPanel
        :datasets="datasets"
        :initial-source="initialSource"
        :initial-type="initialType"
        @filter-change="onFilterChange"
      />
      <DataTable :datasets="filteredDatasets" :loading="loading" />
    </div>

    <footer class="site-footer">
      <p>{{ t('footer') }}</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { t } from '../i18n.js'
import StatsBar from '../components/StatsBar.vue'
import FilterPanel from '../components/FilterPanel.vue'
import DataTable from '../components/DataTable.vue'
import LangSwitcher from '../components/LangSwitcher.vue'

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
  if (sources.length > 0) result = result.filter(d => sources.includes(d.source))
  if (dataTypes.length > 0) result = result.filter(d => (d.data_types || []).some(t => dataTypes.includes(t)))
  if (subtypes.length > 0) result = result.filter(d => (d.tumor_subtypes || []).some(t => subtypes.includes(t)))
  if (pairedOnly) result = result.filter(d => (d.recurrent_sample_count || 0) > 0)
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
  position: relative;
  padding: 2.5rem 2.5rem 2rem;
  overflow: hidden;
}

.header-bg {
  position: absolute;
  inset: 0;
  background: url('https://images.unsplash.com/photo-1530026405186-ed1f139313f8?w=1920&q=80') center/cover no-repeat;
  filter: brightness(0.2) saturate(0.5);
}

.header-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(6,7,20,0.7) 0%, rgba(6,7,20,0.95) 100%),
              linear-gradient(135deg, rgba(11,61,145,0.15) 0%, transparent 60%);
}

.header-inner {
  position: relative;
  z-index: 1;
  max-width: 1400px;
  margin: 0 auto;
}

.header-top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2rem;
}

.back-link {
  display: inline-block;
  color: #a8b8d0;
  text-decoration: none;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  transition: color 0.2s;
}

.back-link:hover { color: #FC3D21; }

.header-badge {
  display: inline-block;
  font-size: 0.6rem;
  font-weight: 800;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: #FC3D21;
  border: 1px solid rgba(252, 61, 33, 0.35);
  padding: 0.3rem 0.8rem;
  border-radius: 2px;
  background: rgba(252, 61, 33, 0.08);
  margin-bottom: 0.8rem;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 900;
  color: #ffffff;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  margin-bottom: 0.4rem;
}

.accent { color: #FC3D21; }

.header-sub {
  color: #a8b8d0;
  font-size: 0.85rem;
  font-weight: 300;
  letter-spacing: 0.03em;
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
  color: #5a6a8a;
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border-top: 1px solid rgba(11, 61, 145, 0.2);
}

@media (max-width: 768px) {
  .page-header { padding: 1.5rem 1rem; }
  .content-area { padding: 1rem; }
  .page-header h1 { font-size: 1.4rem; }
}
</style>
