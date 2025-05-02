<template>
  <div class="min-h-screen bg-black text-white font-sans">
      <!-- Navbar -->
    <header class="flex justify-between items-center px-6 py-4 bg-gray-900 shadow-md">
      <div class="text-green-400 text-xl font-bold flex items-center gap-2">
        <span>🎵</span> SpotifyAlerts
      </div>
      <!-- <nav class="space-x-4">
        <a href="#" class="hover:text-green-400">Home</a>
        <a href="#" class="hover:text-green-400">Settings</a>
        <button class="bg-green-500 text-black px-4 py-1 rounded hover:bg-green-600">Login</button>
      </nav> -->
    </header>

    <!-- Hero Section -->
    <section class="px-6 py-16 grid md:grid-cols-2 gap-12 max-w-6xl mx-auto">
      <div class="flex flex-col justify-center">
        <h1 class="text-4xl md:text-5xl font-bold leading-tight">
          Never Miss a <span class="text-green-400">New Release</span>
        </h1>
        <p class="mt-4 text-lg text-gray-300">
          Get notified instantly when your favorite artists drop new music on Spotify. Choose how you want to be alerted.
        </p>
        <ul class="mt-4 text-green-400 space-x-4 text-sm">
          <li class="inline">Email Alerts</li>
          <li class="inline">SMS Notifications</li>
          <li class="inline">Telegram Messages</li>
        </ul>
      </div>

      <!-- Form Card -->
      <SubscribeForm />
    </section>

    <!-- How it works -->
    <section class="bg-gray-800 py-12">
      <div class="max-w-4xl mx-auto text-center">
        <h3 class="text-2xl font-semibold mb-6">How It Works</h3>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="bg-gray-900 p-6 rounded-lg">
            <h4 class="text-lg font-bold mb-2">1. Subscribe</h4>
            <p class="text-sm text-gray-300">Enter your email and the Spotify artists you want to follow</p>
          </div>
          <div class="bg-gray-900 p-6 rounded-lg">
            <h4 class="text-lg font-bold mb-2">2. Choose Alerts</h4>
            <p class="text-sm text-gray-300">Select how you want to be notified: Email, SMS, or Telegram</p>
          </div>
          <div class="bg-gray-900 p-6 rounded-lg">
            <h4 class="text-lg font-bold mb-2">3. Stay Updated</h4>
            <p class="text-sm text-gray-300">Get instant notifications whenever new music is released</p>
          </div>
        </div>
      </div>
    </section>
      

      <!-- Footer -->
      <footer class="border-t border-gray-800 mt-16 py-6 text-center text-gray-400">
        <p>© {{ new Date().getFullYear() }} SpotifyAlerts. All rights reserved.</p>
      </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SubscribeForm from './components/SubscribeForm.vue'

</script>

<style>
.input {
  @apply w-full px-4 py-2 bg-gray-800 text-white border border-gray-600 rounded focus:outline-none focus:ring-2 focus:ring-green-400;
}
</style>
