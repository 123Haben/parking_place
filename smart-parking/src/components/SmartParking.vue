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

const API_URL = "http://77.47.120.198:8000"
const parkingSpots = ref([])

async function loadParkingData() {
  try {
    const response = await axios.get(API_URL+'/parking_places')
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
    // 1 Besitzer über RFID suchen
    const ownerRes = await axios.get(API_URL+`/owners/by_rfid/${rfId}`);
    const ownerId = ownerRes.data.id;

    if (!ownerId) {
      alert("❌ RFID nicht registriert!");
      return;
    }

    // ⃣ Prüfen, ob dieser Owner schon reserviert hat
    const parkingRes = await axios.get(API_URL+"/parking_places");
    const alreadyReserved = parkingRes.data.some(
        p => p.owner_id === ownerId && p.status === "RESERVED"
    );

    if (alreadyReserved) {
      alert("⚠️ Du hast bereits einen Parkplatz reserviert!");
      return;
    }

    // ⃣Parkplatz reservieren
    const res = await axios.put(
        API_URL+`/parking_places/${parkingId}?status=RESERVED&owner_id=${ownerId}`
    );

    alert(`✅ Parkplatz ${res.data.place_name} erfolgreich reserviert!`);
    await loadParkingData();

  } catch (err) {
    console.error("Fehler bei der Reservierung:", err.response?.data || err.message);
    alert("❌ Fehler bei der Reservierung: " + JSON.stringify(err.response?.data || err.message));
  }
}


async function freeSpot(parkingId) {
  try {
    //  Besitzer löschen (ohne owner_id=null!)
    await axios.put(API_URL+`/parking_places/${parkingId}/owner`);

    // ⃣ Status auf FREE setzen
    await axios.put(API_URL+`/parking_places/${parkingId}?status=FREE`);

    alert("✅ Parkplatz erfolgreich freigegeben!");
    await loadParkingData();
  } catch (err) {
    console.error("Fehler beim Freigeben:", err.response?.data || err.message);
    alert("❌ Fehler beim Freigeben: " + JSON.stringify(err.response?.data || err.message));
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
