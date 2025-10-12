<script setup>
</script>

<template>
  <div class="app-container">
    <div class="dashboard">
      <!-- Sidebar -->
      <div class="sidebar">
        <div class="sidebar-header">
          <h1>Dashboard</h1>
          <p>Analytics & Monitoring</p>
        </div>
        <nav class="sidebar-nav">
          <RouterLink to="/dashboard"><i class="fas fa-home"></i> Dashboard</RouterLink>
          <RouterLink to="/analytics"><i class="fas fa-chart-line"></i> Analytics</RouterLink>
          <RouterLink to="/gate"><i class="fas fa-users"></i> Gate</RouterLink>
          <RouterLink to="/settings"><i class="fas fa-cog"></i> Einstellungen</RouterLink>
        </nav>
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <header class="header">
          <div class="search-container">
            <i class="fas fa-search"></i>
            <input type="text" placeholder="Suchen..." />
          </div>
          <div class="header-actions">
            <button class="notification-btn">
              <i class="fas fa-bell"></i>
              <span class="notification-badge">3</span>
            </button>
            <div class="user-info">
              <div class="user-avatar">U</div>
              <span class="user-name">Gruppe 19</span>
            </div>
          </div>
        </header>

        <main class="dashboard-content">
          <RouterView />
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
