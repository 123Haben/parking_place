<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

// ChartJS registrieren
ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Title, Tooltip, Legend)

// -------------------------
// Reactive State
// -------------------------
const selectedView = ref('day') // Tag / Woche / Monat
const gateLogs = ref([])        // Echte API-Daten
const loading = ref(false)
const error = ref(null)

// -------------------------
// API-Aufruf: /gates
// -------------------------
async function loadGateData() {
  loading.value = true
  error.value = null
  try {
    const res = await axios.get('http://77.47.120.198:8000/gates')
    gateLogs.value = res.data
  } catch (err) {
    console.error(err)
    error.value = 'Fehler beim Laden der Gate-Daten'
  } finally {
    loading.value = false
  }
}

// -------------------------
// Hilfsfunktionen zum Gruppieren
// -------------------------
function countCarsPerHour(logs) {
  const counts = {}
  logs.forEach(log => {
    const hour = new Date(log.open_time).getHours()
    counts[hour] = (counts[hour] || 0) + 1
  })
  return Object.keys(counts).sort((a, b) => a - b).map(h => ({
    label: `${h}:00`,
    value: counts[h]
  }))
}

function countCarsPerDay(logs) {
  const days = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa']
  const counts = {}
  logs.forEach(log => {
    const day = days[new Date(log.open_time).getDay()]
    counts[day] = (counts[day] || 0) + 1
  })
  return days.map(d => ({ label: d, value: counts[d] || 0 }))
}

function countCarsPerMonth(logs) {
  const months = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
  const counts = {}
  logs.forEach(log => {
    const month = new Date(log.open_time).getMonth()
    counts[month] = (counts[month] || 0) + 1
  })
  return months.map((m, i) => ({ label: m, value: counts[i] || 0 }))
}

// -------------------------
// Dynamisches Chart-Data
// -------------------------
const chartData = computed(() => {
  let grouped = []
  if (selectedView.value === 'day') grouped = countCarsPerHour(gateLogs.value)
  if (selectedView.value === 'week') grouped = countCarsPerDay(gateLogs.value)
  if (selectedView.value === 'month') grouped = countCarsPerMonth(gateLogs.value)

  return {
    labels: grouped.map(d => d.label),
    datasets: [
      {
        label:
            selectedView.value === 'day'
                ? 'Autos pro Stunde'
                : selectedView.value === 'week'
                    ? 'Autos pro Tag'
                    : 'Autos pro Monat',
        data: grouped.map(d => d.value),
        borderColor:
            selectedView.value === 'day'
                ? '#1976d2'
                : selectedView.value === 'week'
                    ? '#43a047'
                    : '#f9a825',
        backgroundColor:
            selectedView.value === 'day'
                ? 'rgba(25,118,210,0.2)'
                : selectedView.value === 'week'
                    ? 'rgba(67,160,71,0.2)'
                    : 'rgba(249,168,37,0.2)',
        tension: 0.3,
        fill: true,
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Smart-Parking: Auslastung nach Zeit' },
  },
  scales: {
    y: {
      beginAtZero: true,
      title: { display: true, text: 'Anzahl Autos' },
    },
  },
}

// -------------------------
// Initiales Laden
// -------------------------
onMounted(loadGateData)
</script>

<template>
  <v-card class="pa-4">
    <v-card-title>
      Parkplatz-Auslastung
      <v-spacer />
      <select v-model="selectedView" class="ml-2 pa-1">
        <option value="day">Tag</option>
        <option value="week">Woche</option>
        <option value="month">Monat</option>
      </select>
    </v-card-title>

    <v-card-text>
      <div v-if="loading" class="text-center pa-4">⏳ Daten werden geladen...</div>
      <div v-else-if="error" class="text-error">{{ error }}</div>
      <div v-else>
        <Line :data="chartData" :options="chartOptions" />
      </div>
    </v-card-text>
  </v-card>
</template>
