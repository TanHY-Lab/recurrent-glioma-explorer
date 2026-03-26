<template>
  <div class="lang-switcher">
    <el-select
      :model-value="currentLang"
      @change="setLang"
      size="small"
      style="width: 120px"
    >
      <el-option
        v-for="opt in langOptions"
        :key="opt.value"
        :label="opt.label"
        :value="opt.value"
      />
    </el-select>
  </div>
</template>

<script setup>
import { currentLang, langOptions, setLang } from '../i18n.js'
</script>

<style scoped>
.lang-switcher {
  display: inline-flex;
  align-items: center;
}
</style>
