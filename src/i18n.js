import { ref, computed } from 'vue'

const STORAGE_KEY = 'rg-explorer-lang'

const currentLang = ref(localStorage.getItem(STORAGE_KEY) || 'en')

const messages = {
  en: {
    // Landing page
    badge: 'Multi-Source Aggregation',
    siteTitle: 'Recurrent Glioma',
    siteTitleAccent: 'Multi-Omics',
    siteTitleEnd: 'Explorer',
    subtitle: 'Integrated dataset explorer for recurrent glioma research',
    omicsBar: 'Bulk RNA-seq · scRNA-seq · snRNA-seq · Spatial Transcriptomics · WES/WGS · Methylation · Proteomics',
    viewAll: 'View All Datasets',
    metaInfo: 'Data sources: GEO, GLASS, CGGA, TCGA, CPTAC, cBioPortal · Updated periodically',
    explore: 'EXPLORE',

    // Cards
    geoTitle: 'GEO Database',
    geoDesc: 'Recurrent glioma omics datasets from NCBI Gene Expression Omnibus',
    glassTitle: 'GLASS Consortium',
    glassDesc: 'Glioma Longitudinal AnalySiS — international consortium tracking primary-recurrence paired samples',
    cggaTitle: 'CGGA',
    cggaDesc: 'Chinese Glioma Genome Atlas — large-scale Chinese glioma multi-omics cohort',
    tcgaTitle: 'TCGA / GDC',
    tcgaDesc: 'NCI Genomic Data Commons — LGG/GBM multi-omics data with recurrent samples',
    cptacTitle: 'CPTAC Proteomics',
    cptacDesc: 'Clinical Proteomic Tumor Analysis Consortium — GBM proteomic/phosphoproteomic data',
    cbioTitle: 'cBioPortal',
    cbioDesc: 'Integrated cancer genomics portal with mutation, copy number, and expression data',
    otherTitle: 'Other Sources',
    otherDesc: 'Ivy GAP, REMBRANDT, EORTC, single-center cohorts and supplementary datasets',

    // Explorer page
    backHome: 'Home',
    explorerTitle: 'Recurrent Glioma',
    explorerTitleAccent: 'Multi-Omics',
    explorerTitleEnd: 'Explorer',
    explorerSubtitle: 'Integrated dataset explorer for recurrent glioma research',
    footer: 'Recurrent Glioma Multi-Omics Explorer · Data aggregated from GEO, GLASS, CGGA, TCGA, CPTAC, cBioPortal and other sources',

    // Stats
    statDatasets: 'Datasets',
    statSources: 'Sources',
    statOmics: 'Omics Types',
    statSamples: 'Total Samples',
    statRecurrent: 'Recurrent Samples',

    // Filters
    searchPlaceholder: 'Search datasets...',
    sourcePlaceholder: 'Source',
    dataTypePlaceholder: 'Data Type',
    subtypePlaceholder: 'Subtype',
    pairedLabel: 'Paired',
    resetBtn: 'Reset',
    subtypeAstrocytoma: 'Astrocytoma',
    subtypeOligo: 'Oligodendroglioma',
    subtypeOther: 'Other',

    // Table
    colSource: 'Source',
    colAccession: 'Accession',
    colTitle: 'Title',
    colDataTypes: 'Data Types',
    colSamples: 'Samples',
    colRecurrent: 'Recurrent',
    colSubtypes: 'Subtypes',
    colCountry: 'Country',
    colDate: 'Date',
    showingOf: 'Showing {shown} of {total} datasets',
    expandSummary: 'Summary',
    expandContributors: 'Contributors',
    expandInstitution: 'Institution',

    // Language
    langLabel: 'Language',
  },
  zh: {
    badge: '多源数据聚合',
    siteTitle: '复发胶质瘤',
    siteTitleAccent: '多组学',
    siteTitleEnd: '数据浏览器',
    subtitle: '复发胶质瘤研究综合数据集浏览平台',
    omicsBar: 'Bulk RNA-seq · scRNA-seq · snRNA-seq · 空间转录组 · WES/WGS · 甲基化 · 蛋白质组',
    viewAll: '浏览所有数据集',
    metaInfo: '数据来源：GEO、GLASS、CGGA、TCGA、CPTAC、cBioPortal · 定期更新',
    explore: '浏览',

    geoTitle: 'GEO 数据库',
    geoDesc: 'NCBI Gene Expression Omnibus 中收录的复发胶质瘤组学数据集',
    glassTitle: 'GLASS 联盟',
    glassDesc: 'Glioma Longitudinal AnalySiS，纵向追踪初发-复发配对样本的国际联盟',
    cggaTitle: '中国脑胶质瘤基因组图谱',
    cggaDesc: 'Chinese Glioma Genome Atlas，大规模中国胶质瘤多组学队列',
    tcgaTitle: 'TCGA 癌症基因组图谱',
    tcgaDesc: 'NCI Genomic Data Commons，LGG/GBM 多组学数据及复发样本',
    cptacTitle: 'CPTAC 蛋白质组学',
    cptacDesc: 'Clinical Proteomic Tumor Analysis Consortium，GBM 蛋白/磷酸化组学',
    cbioTitle: 'cBioPortal 门户',
    cbioDesc: '综合癌症基因组门户网站，含突变、拷贝数、表达等多维数据',
    otherTitle: '其他数据来源',
    otherDesc: 'Ivy GAP、REMBRANDT、EORTC、单中心队列及文献附属数据集等',

    backHome: '首页',
    explorerTitle: '复发胶质瘤',
    explorerTitleAccent: '多组学',
    explorerTitleEnd: '数据浏览器',
    explorerSubtitle: '复发胶质瘤研究综合数据集浏览平台',
    footer: '复发胶质瘤多组学数据浏览器 · 数据聚合自 GEO、GLASS、CGGA、TCGA、CPTAC、cBioPortal 等多个来源',

    statDatasets: '数据集',
    statSources: '数据来源',
    statOmics: '组学类型',
    statSamples: '总样本数',
    statRecurrent: '复发样本',

    searchPlaceholder: '搜索数据集...',
    sourcePlaceholder: '数据来源',
    dataTypePlaceholder: '数据类型',
    subtypePlaceholder: '肿瘤亚型',
    pairedLabel: '配对',
    resetBtn: '重置',
    subtypeAstrocytoma: '星形细胞瘤',
    subtypeOligo: '少突胶质细胞瘤',
    subtypeOther: '其他',

    colSource: '来源',
    colAccession: '编号',
    colTitle: '标题',
    colDataTypes: '数据类型',
    colSamples: '样本数',
    colRecurrent: '复发',
    colSubtypes: '亚型',
    colCountry: '国家',
    colDate: '日期',
    showingOf: '显示 {shown} / {total} 个数据集',
    expandSummary: '摘要',
    expandContributors: '贡献者',
    expandInstitution: '机构',

    langLabel: '语言',
  },
  fr: {
    badge: 'Agrégation multi-sources',
    siteTitle: 'Gliome récurrent',
    siteTitleAccent: 'Multi-omique',
    siteTitleEnd: 'Explorateur',
    subtitle: 'Explorateur intégré de jeux de données pour la recherche sur les gliomes récurrents',
    omicsBar: 'Bulk RNA-seq · scRNA-seq · snRNA-seq · Transcriptomique spatiale · WES/WGS · Méthylation · Protéomique',
    viewAll: 'Voir tous les jeux de données',
    metaInfo: 'Sources : GEO, GLASS, CGGA, TCGA, CPTAC, cBioPortal · Mis à jour périodiquement',
    explore: 'EXPLORER',

    geoTitle: 'Base GEO',
    geoDesc: 'Jeux de données omiques de gliomes récurrents du NCBI Gene Expression Omnibus',
    glassTitle: 'Consortium GLASS',
    glassDesc: 'Glioma Longitudinal AnalySiS — consortium international de suivi des échantillons appariés',
    cggaTitle: 'CGGA',
    cggaDesc: 'Chinese Glioma Genome Atlas — grande cohorte multi-omique de gliomes chinois',
    tcgaTitle: 'TCGA / GDC',
    tcgaDesc: 'NCI Genomic Data Commons — données multi-omiques LGG/GBM avec échantillons récurrents',
    cptacTitle: 'Protéomique CPTAC',
    cptacDesc: 'Clinical Proteomic Tumor Analysis Consortium — données protéomiques et phosphoprotéomiques du GBM',
    cbioTitle: 'cBioPortal',
    cbioDesc: 'Portail intégré de génomique du cancer avec données de mutations, nombre de copies et expression',
    otherTitle: 'Autres sources',
    otherDesc: 'Ivy GAP, REMBRANDT, EORTC, cohortes monocentriques et jeux de données supplémentaires',

    backHome: 'Accueil',
    explorerTitle: 'Gliome récurrent',
    explorerTitleAccent: 'Multi-omique',
    explorerTitleEnd: 'Explorateur',
    explorerSubtitle: 'Explorateur intégré de jeux de données pour la recherche sur les gliomes récurrents',
    footer: 'Explorateur Multi-Omique des Gliomes Récurrents · Données agrégées de GEO, GLASS, CGGA, TCGA, CPTAC, cBioPortal et autres sources',

    statDatasets: 'Jeux de données',
    statSources: 'Sources',
    statOmics: 'Types omiques',
    statSamples: 'Échantillons totaux',
    statRecurrent: 'Échantillons récurrents',

    searchPlaceholder: 'Rechercher des jeux de données...',
    sourcePlaceholder: 'Source',
    dataTypePlaceholder: 'Type de données',
    subtypePlaceholder: 'Sous-type',
    pairedLabel: 'Appariés',
    resetBtn: 'Réinitialiser',
    subtypeAstrocytoma: 'Astrocytome',
    subtypeOligo: 'Oligodendrogliome',
    subtypeOther: 'Autre',

    colSource: 'Source',
    colAccession: 'Accession',
    colTitle: 'Titre',
    colDataTypes: 'Types de données',
    colSamples: 'Échantillons',
    colRecurrent: 'Récurrents',
    colSubtypes: 'Sous-types',
    colCountry: 'Pays',
    colDate: 'Date',
    showingOf: 'Affichage de {shown} sur {total} jeux de données',
    expandSummary: 'Résumé',
    expandContributors: 'Contributeurs',
    expandInstitution: 'Institution',

    langLabel: 'Langue',
  },
  de: {
    badge: 'Multi-Quellen-Aggregation',
    siteTitle: 'Rezidiv-Gliom',
    siteTitleAccent: 'Multi-Omik',
    siteTitleEnd: 'Explorer',
    subtitle: 'Integrierter Datensatz-Explorer für die Forschung an rezidivierenden Gliomen',
    omicsBar: 'Bulk RNA-seq · scRNA-seq · snRNA-seq · Räumliche Transkriptomik · WES/WGS · Methylierung · Proteomik',
    viewAll: 'Alle Datensätze anzeigen',
    metaInfo: 'Datenquellen: GEO, GLASS, CGGA, TCGA, CPTAC, cBioPortal · Regelmäßig aktualisiert',
    explore: 'ERKUNDEN',

    geoTitle: 'GEO-Datenbank',
    geoDesc: 'Rezidiv-Gliom-Omik-Datensätze aus dem NCBI Gene Expression Omnibus',
    glassTitle: 'GLASS-Konsortium',
    glassDesc: 'Glioma Longitudinal AnalySiS — internationales Konsortium zur Verfolgung von Primär-Rezidiv-Probenpaaren',
    cggaTitle: 'CGGA',
    cggaDesc: 'Chinese Glioma Genome Atlas — groß angelegte chinesische Gliom-Multi-Omik-Kohorte',
    tcgaTitle: 'TCGA / GDC',
    tcgaDesc: 'NCI Genomic Data Commons — LGG/GBM Multi-Omik-Daten mit Rezidivproben',
    cptacTitle: 'CPTAC-Proteomik',
    cptacDesc: 'Clinical Proteomic Tumor Analysis Consortium — GBM-Proteom-/Phosphoproteom-Daten',
    cbioTitle: 'cBioPortal',
    cbioDesc: 'Integriertes Krebsgenomik-Portal mit Mutations-, Kopienzahl- und Expressionsdaten',
    otherTitle: 'Weitere Quellen',
    otherDesc: 'Ivy GAP, REMBRANDT, EORTC, monozentrische Kohorten und ergänzende Datensätze',

    backHome: 'Startseite',
    explorerTitle: 'Rezidiv-Gliom',
    explorerTitleAccent: 'Multi-Omik',
    explorerTitleEnd: 'Explorer',
    explorerSubtitle: 'Integrierter Datensatz-Explorer für die Forschung an rezidivierenden Gliomen',
    footer: 'Rezidiv-Gliom Multi-Omik Explorer · Daten aggregiert aus GEO, GLASS, CGGA, TCGA, CPTAC, cBioPortal und anderen Quellen',

    statDatasets: 'Datensätze',
    statSources: 'Quellen',
    statOmics: 'Omik-Typen',
    statSamples: 'Proben gesamt',
    statRecurrent: 'Rezidivproben',

    searchPlaceholder: 'Datensätze suchen...',
    sourcePlaceholder: 'Quelle',
    dataTypePlaceholder: 'Datentyp',
    subtypePlaceholder: 'Subtyp',
    pairedLabel: 'Gepaart',
    resetBtn: 'Zurücksetzen',
    subtypeAstrocytoma: 'Astrozytom',
    subtypeOligo: 'Oligodendrogliom',
    subtypeOther: 'Sonstige',

    colSource: 'Quelle',
    colAccession: 'Kennung',
    colTitle: 'Titel',
    colDataTypes: 'Datentypen',
    colSamples: 'Proben',
    colRecurrent: 'Rezidiv',
    colSubtypes: 'Subtypen',
    colCountry: 'Land',
    colDate: 'Datum',
    showingOf: '{shown} von {total} Datensätzen angezeigt',
    expandSummary: 'Zusammenfassung',
    expandContributors: 'Mitwirkende',
    expandInstitution: 'Institution',

    langLabel: 'Sprache',
  }
}

const langOptions = [
  { value: 'en', label: 'English' },
  { value: 'zh', label: '中文' },
  { value: 'fr', label: 'Français' },
  { value: 'de', label: 'Deutsch' },
]

function setLang(lang) {
  currentLang.value = lang
  localStorage.setItem(STORAGE_KEY, lang)
}

function t(key) {
  return (messages[currentLang.value] && messages[currentLang.value][key]) || messages.en[key] || key
}

export { currentLang, langOptions, setLang, t }
