<template>
  <div class="container">
    <div class="header">
      <h1>🚗 Smart Parking Status</h1>
      <p>Echtzeit-Übersicht der Parkplatzbelegung</p>
    </div>

    <div class="parking-grid">
      <div
          v-for="spot in parkingSpots"
          :key="spot.id"
          class="parking-spot"
          :class="spot.status.toLowerCase()"
      >
        <div class="spot-number">{{ spot.place_name }}</div>

        <div class="parking-icon">
          <span v-if="spot.status === 'OCCUPIED'" style="color: red;">🚗</span>
          <span v-else-if="spot.status === 'RESERVED'" style="color: orange;">🔒</span>
          <span v-else style="color: green;">🅿️</span>
        </div>

        <div class="status-indicator">
          {{ statusLabel(spot.status) }}
        </div>


        <button
            v-if="spot.status === 'FREE'"
            @click="reserveSpot(spot.id)"
            class="action-button"
        >
          Reservieren
        </button>

        <button
            v-else-if="spot.status === 'RESERVED'"
            @click="freeSpot(spot.id)"
            class="action-button"
        >
          Freigeben
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios"
import { ref, onMounted } from "vue"

const API_URL = "http://77.47.120.198:8000/parking_places"
const parkingSpots = ref([])

async function loadParkingData() {
  try {
    const response = await axios.get(API_URL)
    parkingSpots.value = response.data
  } catch (err) {
    console.warn("⚠️ API nicht erreichbar:", err.message)
  }
}

function statusLabel(status) {
  switch (status) {
    case "FREE": return "Frei"
    case "RESERVED": return "Reserviert"
    case "OCCUPIED": return "Besetzt"
    default: return "Unbekannt"
  }
}

async function reserveSpot(parkingId) {
  const rfId = prompt("Bitte RFID-Tag eingeben:");
  if (!rfId) return;

  try {
    // 1️⃣ RFID -> Besitzer-ID abfragen
    const ownerRes = await axios.get(`http://77.47.120.198:8000/owners/by_rfid/${rfId}`);
    const ownerId = ownerRes.data.id;

    if (!ownerId) {
      alert("RFID nicht registriert!");
      return;
    }

    // 2️⃣ Besitzer zuweisen (korrektes PUT)
    await axios.put(
        `http://77.47.120.198:8000/parking_places/${parkingId}/owner?owner_id=${ownerId}`,
        null,
        { headers: { "Content-Type": "application/json" } }
    );

    // 3️⃣ Status auf RESERVED setzen
    await axios.put(
        `http://77.47.120.198:8000/parking_places/${parkingId}`,
        { status: "RESERVED" },
        { headers: { "Content-Type": "application/json" } }
    );

    alert("✅ Parkplatz erfolgreich reserviert!");
    await loadParkingData();
  } catch (err) {
    console.error(err);
    alert("❌ Fehler bei der Reservierung: " + err.message);
  }
}

async function freeSpot(parkingId) {
  try {
    // 1️⃣ Besitzer entfernen
    await axios.put(
        `http://77.47.120.198:8000/parking_places/${parkingId}/owner?owner_id=`,
        null,
        { headers: { "Content-Type": "application/json" } }
    );

    // 2️⃣ Status auf FREE setzen
    await axios.put(
        `http://77.47.120.198:8000/parking_places/${parkingId}`,
        { status: "FREE" },
        { headers: { "Content-Type": "application/json" } }
    );

    alert("✅ Parkplatz freigegeben!");
    await loadParkingData();
  } catch (err) {
    console.error(err);
    alert("❌ Fehler beim Freigeben: " + err.message);
  }
}


onMounted(() => {
  loadParkingData()
  setInterval(loadParkingData, 3000)
})
</script>

<style scoped>
.action-button {
  padding: 8px 16px;
  font-size: 0.9rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  margin-top: 8px;
}
</style>
