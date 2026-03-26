<template>
  <div class="filter-panel">
    <div class="filter-row">
      <!-- Keyword Search -->
      <div class="filter-item keyword-search">
        <el-input
          v-model="keyword"
          :placeholder="t('searchPlaceholder')"
          clearable
          :prefix-icon="Search"
          @input="emitFilters"
          @clear="emitFilters"
        />
      </div>

      <!-- Source Filter -->
      <div class="filter-item">
        <el-select
          v-model="selectedSources"
          multiple
          collapse-tags
          collapse-tags-tooltip
          :placeholder="t('sourcePlaceholder')"
          clearable
          @change="emitFilters"
        >
          <el-option
            v-for="source in availableSources"
            :key="source"
            :label="source"
            :value="source"
          />
        </el-select>
      </div>

      <!-- Data Type Filter -->
      <div class="filter-item">
        <el-select
          v-model="selectedDataTypes"
          multiple
          collapse-tags
          collapse-tags-tooltip
          :placeholder="t('dataTypePlaceholder')"
          clearable
          @change="emitFilters"
        >
          <el-option
            v-for="dt in availableDataTypes"
            :key="dt"
            :label="dt"
            :value="dt"
          />
        </el-select>
      </div>

      <!-- Tumor Subtype Filter -->
      <div class="filter-item">
        <el-select
          v-model="selectedSubtypes"
          multiple
          collapse-tags
          collapse-tags-tooltip
          :placeholder="t('subtypePlaceholder')"
          clearable
          @change="emitFilters"
        >
          <el-option label="GBM" value="GBM" />
          <el-option :label="t('subtypeAstrocytoma')" value="Astrocytoma" />
          <el-option :label="t('subtypeOligo')" value="Oligodendroglioma" />
          <el-option :label="t('subtypeOther')" value="Other" />
        </el-select>
      </div>

      <!-- Paired Samples Toggle -->
      <div class="filter-item paired-toggle">
        <el-switch
          v-model="pairedOnly"
          :active-text="t('pairedLabel')"
          @change="emitFilters"
        />
      </div>

      <!-- Reset Button -->
      <div class="filter-item">
        <el-button @click="resetFilters">{{ t('resetBtn') }}</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { t } from '../i18n.js'

const props = defineProps({
  datasets: { type: Array, default: () => [] },
  initialSource: { type: String, default: '' },
  initialType: { type: String, default: '' }
})

const emit = defineEmits(['filter-change'])

const keyword = ref('')
const selectedSources = ref([])
const selectedDataTypes = ref([])
const selectedSubtypes = ref([])
const pairedOnly = ref(false)

const availableSources = computed(() => {
  const sources = new Set(props.datasets.map(d => d.source).filter(Boolean))
  return [...sources].sort()
})

const availableDataTypes = computed(() => {
  const types = new Set()
  props.datasets.forEach(d => {
    (d.data_types || []).forEach(t => types.add(t))
  })
  return [...types].sort()
})

function emitFilters() {
  emit('filter-change', {
    keyword: keyword.value,
    sources: selectedSources.value,
    dataTypes: selectedDataTypes.value,
    subtypes: selectedSubtypes.value,
    pairedOnly: pairedOnly.value
  })
}

function resetFilters() {
  keyword.value = ''
  selectedSources.value = []
  selectedDataTypes.value = []
  selectedSubtypes.value = []
  pairedOnly.value = false
  emitFilters()
}

// Apply initial filters from URL params once datasets are loaded
watch(() => props.datasets.length, (len) => {
  if (len > 0) {
    if (props.initialSource) {
      selectedSources.value = [props.initialSource]
    }
    if (props.initialType) {
      selectedSubtypes.value = [props.initialType]
    }
    if (props.initialSource || props.initialType) {
      emitFilters()
    }
  }
}, { immediate: true })
</script>

<style scoped>
.filter-panel {
  background: #131a3e;
  border: 1px solid rgba(0, 212, 170, 0.1);
  border-radius: 6px;
  padding: 1rem 1.2rem;
  margin-bottom: 1.5rem;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  align-items: center;
}

.filter-item {
  flex-shrink: 0;
}

.keyword-search {
  flex: 1;
  min-width: 220px;
}

.filter-item :deep(.el-select) {
  min-width: 180px;
}

.paired-toggle {
  display: flex;
  align-items: center;
}

.paired-toggle :deep(.el-switch__label) {
  color: #8892b0 !important;
  font-size: 0.78rem;
}

.paired-toggle :deep(.el-switch__label.is-active) {
  color: #00d4aa !important;
}

@media (max-width: 768px) {
  .filter-row { flex-direction: column; }
  .filter-item { width: 100%; }
  .filter-item :deep(.el-select) { min-width: unset; width: 100%; }
}
</style>
