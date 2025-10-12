<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import '../assets/gate.css'

// Reaktive States
const activeTab = ref('current')
const gates = ref([])
const owners = ref([]) // Neue Tabelle mit registrierten RFID-Tags
const loading = ref(false)
const error = ref(null)

// Formularfelder
const newOwner = ref({
  rf_id_tag: '',
  owner_name: '',
  contact: '',
  vehicle_name: '',
})

// API-Abruf
async function loadGates() {
  loading.value = true
  try {
    const res = await axios.get('http://77.47.120.198:8000/gates')
    gates.value = res.data
  } catch (err) {
    error.value = 'Fehler beim Laden der Gate-Daten'
  } finally {
    loading.value = false
  }
}

// RFID-Registrierung abrufen
async function loadOwners() {
  try {
    const res = await axios.get('http://77.47.120.198:8000/owners/')
    owners.value = res.data
  } catch (err) {
    console.warn('⚠️ Konnte Besitzer nicht laden:', err)
  }
}

// Formular absenden
async function registerOwner() {
  if (!newOwner.value.rf_id_tag || !newOwner.value.owner_name) {
    alert('Bitte mindestens RFID-Tag und Name eingeben!')
    return
  }

  try {
    const res = await axios.post('http://77.47.120.198:8000/owners/', {
      rf_id_tag: newOwner.value.rf_id_tag,
      owner_name: newOwner.value.owner_name,
    })
    alert('✅ RFID-Tag erfolgreich registriert!')
    owners.value.push(res.data) // zur Tabelle hinzufügen
    newOwner.value = { rf_id_tag: '', owner_name: '', contact: '', vehicle_name: '' } // Reset
  } catch (err) {
    alert('❌ Fehler bei der Registrierung: ' + err.message)
  }
}

// Anzeige
const currentVehicles = computed(() => gates.value.filter(g => !g.exit_time))
const historyVehicles = computed(() => gates.value.filter(g => g.exit_time))

function formatDateTime(dateTime) {
  if (!dateTime) return '-'
  const d = new Date(dateTime)
  return d.toLocaleString('de-DE', { hour: '2-digit', minute: '2-digit' })
}

function calcDuration(open, exit) {
  if (!open || !exit) return '-'
  const diffMs = new Date(exit) - new Date(open)
  const totalSeconds = Math.floor(diffMs / 1000)
  const h = Math.floor(totalSeconds / 3600)
  const m = Math.floor((totalSeconds % 3600) / 60)
  const s = totalSeconds % 60
  if (h > 0) return `${h}h ${m}min ${s}s`
  if (m > 0) return `${m}min ${s}s`
  return `${s}s`
}

onMounted(() => {
  loadGates()
  loadOwners()
})
</script>

<template>
  <div class="container">
    <div class="header">
      <h1>🚗 Smart Parking – Fahrzeugverwaltung</h1>
      <p>Übersicht aller Fahrzeuge und Parkplatznutzung</p>
    </div>

    <!-- Tab Navigation -->
    <div class="tabs">
      <button
          class="tab-button"
          :class="{ active: activeTab === 'current' }"
          @click="activeTab = 'current'"
      >
        Aktuelle Fahrzeuge
      </button>
      <button
          class="tab-button"
          :class="{ active: activeTab === 'history' }"
          @click="activeTab = 'history'"
      >
        Historie
      </button>
      <button
          class="tab-button"
          :class="{ active: activeTab === 'register' }"
          @click="activeTab = 'register'"
      >
        RFID-Registrierung
      </button>
    </div>

    <!-- Ladezustand -->
    <div v-if="loading" class="text-center pa-4">⏳ Daten werden geladen...</div>
    <div v-else-if="error" class="text-error pa-4">{{ error }}</div>

    <!-- Aktuelle Fahrzeuge -->

    <div v-else-if="activeTab === 'current'" class="tab-content active">
      <div class="table-container">
        <table>
          <thead>
          <tr>
            <th>ID</th>
            <th>RFID-Tag</th>
            <th>Ankunftszeit</th>
            <th>Status</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="g in currentVehicles" :key="g.id">
            <td>{{ g.id }}</td>
            <td>{{ g.rf_id_tag }}</td>
            <td>{{ formatDateTime(g.open_time) }}</td>
            <td><span class="status-badge status-occupied">Besetzt</span></td>
          </tr>
          <tr v-if="!currentVehicles.length">
            <td colspan="4" class="text-center">Keine aktiven Fahrzeuge</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Historie -->
    <div v-else-if="activeTab === 'history'" class="tab-content active">
    <div class="table-container">
        <table>
          <thead>
          <tr>
            <th>ID</th>
            <th>RFID-Tag</th>
            <th>Ankunft</th>
            <th>Abfahrt</th>
            <th>Dauer</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="g in historyVehicles" :key="g.id">
            <td>{{ g.id }}</td>
            <td>{{ g.rf_id_tag }}</td>
            <td>{{ formatDateTime(g.open_time) }}</td>
            <td>{{ formatDateTime(g.exit_time) }}</td>
            <td>{{ calcDuration(g.open_time, g.exit_time) }}</td>
          </tr>
          <tr v-if="!historyVehicles.length">
            <td colspan="5" class="text-center">Noch keine Historie</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- register -->
    <div v-else-if="activeTab === 'register'" class="tab-content active">
      <div class="registration-form">
        <h2 class="form-title">Neues RFID-Tag registrieren</h2>

        <form @submit.prevent="registerOwner">
          <div class="form-group">
            <label>RFID-Tag *</label>
            <input v-model="newOwner.rf_id_tag" type="text" placeholder="z.B. RFID-007-STU" required>
          </div>

          <div class="form-group">
            <label>Besitzername *</label>
            <input v-model="newOwner.owner_name" type="text" placeholder="z.B. Max Mustermann" required>
          </div>

          <div class="form-group">
            <label>Fahrzeugname (optional)</label>
            <input v-model="newOwner.vehicle_name" type="text" placeholder="z.B. BMW X5, VW Passat">
          </div>

          <div class="form-group">
            <label>Kontakt (optional)</label>
            <input v-model="newOwner.contact" type="text" placeholder="Telefonnummer oder E-Mail">
          </div>

          <button type="submit" class="submit-button">RFID-Tag registrieren</button>
        </form>
      </div>

      <div class="table-container">
        <table>
          <thead>
          <tr>
            <th>RFID-Tag</th>
            <th>Besitzer</th>
            <th>Registriert am</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="o in owners" :key="o.id">
            <td>{{ o.rf_id_tag }}</td>
            <td>{{ o.owner_name }}</td>
            <td>{{ formatDateTime(o.created_at) }}</td>
          </tr>
          <tr v-if="!owners.length">
            <td colspan="3" class="text-center">Noch keine Registrierungen</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
