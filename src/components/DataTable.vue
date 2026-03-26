<template>
  <div class="data-table-wrapper">
    <el-table
      :data="paginatedData"
      v-loading="loading"
      stripe
      highlight-current-row
      row-key="accession"
      :default-sort="{ prop: 'publication_date', order: 'descending' }"
      @sort-change="onSortChange"
      @row-click="toggleExpand"
      ref="tableRef"
      style="width: 100%"
    >
      <!-- Expand -->
      <el-table-column type="expand">
        <template #default="{ row }">
          <div class="expand-content">
            <div v-if="row.summary" class="expand-section">
              <div class="expand-label">Summary / 摘要</div>
              <div class="expand-text">{{ row.summary }}</div>
            </div>
            <div class="expand-meta">
              <div v-if="row.contributors" class="expand-section">
                <div class="expand-label">Contributors / 贡献者</div>
                <div class="expand-text">{{ row.contributors }}</div>
              </div>
              <div v-if="row.institution" class="expand-section">
                <div class="expand-label">Institution / 机构</div>
                <div class="expand-text">{{ row.institution }}</div>
              </div>
              <div v-if="row.pubmed_ids && row.pubmed_ids.length" class="expand-section">
                <div class="expand-label">PubMed</div>
                <div class="expand-text">
                  <a
                    v-for="pmid in row.pubmed_ids"
                    :key="pmid"
                    :href="`https://pubmed.ncbi.nlm.nih.gov/${pmid}/`"
                    target="_blank"
                    rel="noopener"
                    class="pubmed-link"
                  >
                    PMID: {{ pmid }}
                  </a>
                </div>
              </div>
              <div v-if="row.source_url" class="expand-section">
                <div class="expand-label">Source URL</div>
                <div class="expand-text">
                  <a :href="row.source_url" target="_blank" rel="noopener" class="source-link">{{ row.source_url }}</a>
                </div>
              </div>
            </div>
          </div>
        </template>
      </el-table-column>

      <!-- Source -->
      <el-table-column prop="source" label="Source" sortable="custom" width="110">
        <template #default="{ row }">
          <el-tag size="small" type="primary">{{ row.source }}</el-tag>
        </template>
      </el-table-column>

      <!-- Accession -->
      <el-table-column prop="accession" label="Accession" sortable="custom" width="140">
        <template #default="{ row }">
          <a v-if="row.source_url" :href="row.source_url" target="_blank" rel="noopener" class="accession-link" @click.stop>
            {{ row.accession }}
          </a>
          <span v-else>{{ row.accession }}</span>
        </template>
      </el-table-column>

      <!-- Title -->
      <el-table-column prop="title" label="Title / 标题" sortable="custom" min-width="280" show-overflow-tooltip>
        <template #default="{ row }">
          <span class="title-text">{{ row.title }}</span>
        </template>
      </el-table-column>

      <!-- Data Types -->
      <el-table-column label="Data Types / 数据类型" width="200">
        <template #default="{ row }">
          <div class="tag-group">
            <el-tag
              v-for="dt in (row.data_types || []).slice(0, 3)"
              :key="dt"
              size="small"
              :type="dataTypeTagType(dt)"
              class="data-tag"
            >
              {{ dt }}
            </el-tag>
            <el-tag
              v-if="(row.data_types || []).length > 3"
              size="small"
              type="info"
              class="data-tag"
            >
              +{{ row.data_types.length - 3 }}
            </el-tag>
          </div>
        </template>
      </el-table-column>

      <!-- Sample Count -->
      <el-table-column prop="sample_count" label="Samples" sortable="custom" width="100" align="right">
        <template #default="{ row }">
          <span class="num-value">{{ (row.sample_count || 0).toLocaleString() }}</span>
        </template>
      </el-table-column>

      <!-- Recurrent Samples -->
      <el-table-column prop="recurrent_sample_count" label="Recurrent" sortable="custom" width="105" align="right">
        <template #default="{ row }">
          <span class="num-value accent" v-if="row.recurrent_sample_count">{{ row.recurrent_sample_count.toLocaleString() }}</span>
          <span class="num-value muted" v-else>-</span>
        </template>
      </el-table-column>

      <!-- Tumor Subtypes -->
      <el-table-column label="Subtypes / 亚型" width="190">
        <template #default="{ row }">
          <div class="tag-group">
            <el-tag
              v-for="st in (row.tumor_subtypes || []).slice(0, 3)"
              :key="st"
              size="small"
              type="warning"
              class="data-tag"
            >
              {{ st }}
            </el-tag>
            <el-tag
              v-if="(row.tumor_subtypes || []).length > 3"
              size="small"
              type="info"
              class="data-tag"
            >
              +{{ row.tumor_subtypes.length - 3 }}
            </el-tag>
          </div>
        </template>
      </el-table-column>

      <!-- Country -->
      <el-table-column prop="country" label="Country" sortable="custom" width="100" />

      <!-- Date -->
      <el-table-column prop="publication_date" label="Date" sortable="custom" width="110">
        <template #default="{ row }">
          <span class="date-text">{{ row.publication_date || '-' }}</span>
        </template>
      </el-table-column>
    </el-table>

    <!-- Pagination -->
    <div class="pagination-bar">
      <div class="result-info">
        Showing {{ paginatedData.length }} of {{ sortedData.length }} datasets
      </div>
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[20, 50, 100, 200]"
        :total="sortedData.length"
        layout="sizes, prev, pager, next, jumper"
        background
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  datasets: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false }
})

const tableRef = ref(null)
const currentPage = ref(1)
const pageSize = ref(20)
const sortProp = ref('publication_date')
const sortOrder = ref('descending')

// Reset page when datasets change
watch(() => props.datasets.length, () => {
  currentPage.value = 1
})

function onSortChange({ prop, order }) {
  sortProp.value = prop
  sortOrder.value = order
  currentPage.value = 1
}

const sortedData = computed(() => {
  const data = [...props.datasets]
  if (!sortProp.value || !sortOrder.value) return data

  const prop = sortProp.value
  const asc = sortOrder.value === 'ascending'

  data.sort((a, b) => {
    let va = a[prop]
    let vb = b[prop]

    if (va == null) va = ''
    if (vb == null) vb = ''

    if (typeof va === 'number' && typeof vb === 'number') {
      return asc ? va - vb : vb - va
    }

    va = String(va).toLowerCase()
    vb = String(vb).toLowerCase()
    if (va < vb) return asc ? -1 : 1
    if (va > vb) return asc ? 1 : -1
    return 0
  })

  return data
})

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return sortedData.value.slice(start, start + pageSize.value)
})

function toggleExpand(row) {
  if (tableRef.value) {
    tableRef.value.toggleRowExpansion(row)
  }
}

function dataTypeTagType(dt) {
  const dtLower = (dt || '').toLowerCase()
  if (dtLower.includes('rna-seq') || dtLower.includes('rnaseq') || dtLower.includes('bulk rna')) return 'primary'
  if (dtLower.includes('scrna') || dtLower.includes('single-cell') || dtLower.includes('snrna')) return 'success'
  if (dtLower.includes('spatial')) return 'warning'
  if (dtLower.includes('wes') || dtLower.includes('wgs') || dtLower.includes('exome') || dtLower.includes('mutation')) return 'danger'
  if (dtLower.includes('methylation') || dtLower.includes('atac')) return 'info'
  return 'primary'
}
</script>

<style scoped>
.data-table-wrapper {
  margin-bottom: 2rem;
}

.tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.data-tag {
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.accession-link {
  color: #00d4aa;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.85rem;
  letter-spacing: 0.02em;
}

.accession-link:hover {
  text-decoration: underline;
}

.title-text {
  font-size: 0.85rem;
  line-height: 1.4;
}

.num-value {
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  font-size: 0.88rem;
}

.num-value.accent { color: #00d4aa; }
.num-value.muted { color: #4a5580; }

.date-text {
  font-size: 0.82rem;
  color: #8892b0;
}

/* Expand content */
.expand-content {
  padding: 1rem 1.5rem;
  background: #0c1230;
  border-radius: 4px;
}

.expand-section {
  margin-bottom: 0.8rem;
}

.expand-section:last-child {
  margin-bottom: 0;
}

.expand-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #00d4aa;
  font-weight: 600;
  margin-bottom: 0.3rem;
}

.expand-text {
  font-size: 0.84rem;
  color: #c8d6e5;
  line-height: 1.6;
}

.expand-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.8rem;
}

.pubmed-link, .source-link {
  color: #00d4aa;
  text-decoration: none;
  margin-right: 1rem;
  font-size: 0.82rem;
}

.pubmed-link:hover, .source-link:hover {
  text-decoration: underline;
}

/* Pagination */
.pagination-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.result-info {
  font-size: 0.78rem;
  color: #8892b0;
  letter-spacing: 0.03em;
}

@media (max-width: 768px) {
  .pagination-bar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
