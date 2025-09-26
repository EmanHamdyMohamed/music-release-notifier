<template>
  <div class="bg-gray-900 border border-gray-700 rounded-xl p-6 w-full">
    <h2 class="text-xl font-semibold mb-4">Subscribe to Artist Updates</h2>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <input v-model="form.email" type="email" @blur="getSubscription" placeholder="Your Email" required class="input" />

      <MultiSelectDropdown
      :initial-selected="form.subscribed_artists"
      value-field="id"
      label-field="name"
      placeholder="Search artists..."
      :min-search-chars="3"
      @update:selected="form.subscribed_artists = $event"
      class="mb-6"
    />

      <!-- Notification Methods -->
      <div class="space-y-2">
        <div class="flex items-center gap-2">
          <input type="checkbox" value="email" v-model="form.notification_methods" id="emailMethod" />
          <label for="emailMethod" class="text-sm">Get notified by email</label>
        </div>

        <div class="flex items-center gap-2">
          <input type="checkbox" value="sms" v-model="form.notification_methods" id="smsMethod" />
          <label for="smsMethod" class="text-sm">Get notified by SMS</label>
        </div>
        <input v-if="form.notification_methods.includes('sms')" required="form.notification_methods.includes('sms')" v-model="form.phone_number" placeholder="+1234567890" class="input" />

        <div class="flex items-center gap-2">
          <input type="checkbox" value="telegram" v-model="form.notification_methods" id="telegramMethod" />
          <label for="telegramMethod" class="text-sm">Get notified via Telegram</label>
        </div>
        <input v-if="form.notification_methods.includes('telegram')" required="form.notification_methods.includes('telegram')" v-model="form.telegram_chat_id" placeholder="Telegram Chat ID" class="input" />
      </div>

      <button type="submit" class="w-full bg-green-500 hover:bg-green-600 text-black font-semibold py-2 rounded">
        Subscribe
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import MultiSelectDropdown from './ArtistSearch.vue' // your vue-multiselect wrapper
import { toast } from 'vue3-toastify'
import config from '../config.js'

const form = ref({
  email: '',
  subscribed_artists: [],
  notification_methods: [],
  phone_number: '',
  telegram_chat_id: ''

})

const getSubscription = async () => {
  if (!form.value.email) {
    return
  }
  try {
    console.log('config.getApiUrl(config.endpoints.subscribe) ===> ', config.getApiUrl(config.endpoints.subscribe))
    const response = await axios.get(config.getApiUrl(config.endpoints.subscribe), {
      params: {
        email: form.value.email
      }
    })
    console.log('Response:', response.data)
    form.value.subscribed_artists = response.data.subscribed_artists
    form.value.notification_methods = response.data.notification_methods
    form.value.phone_number = response.data.phone_number
    form.value.telegram_chat_id = response.data.telegram_chat_id

  } catch (err) {
    console.error('Error getting subscription:', err)
    toast.error("❌ Subscription failed!")
  }
}

const handleSubmit = async () => {
  try {
    if (!form.value.notification_methods.length) {
      toast.error('⚠️ Please select at least one notification method.')
      return
    }

    if (!form.value.subscribed_artists.length) {
      toast.error('🎧 Please select at least one artist.')
      return
    }
    const payload = {
      email: form.value.email,
      subscribed_artists: form.value.subscribed_artists.map(a => ({
        id: a.id,
        name: a.name
      })),
      notification_methods: form.value.notification_methods,
      phone_number: form.value.phone_number,
      telegram_chat_id: form.value.telegram_chat_id
    }
    // request subscription api
    const response = await axios.post(config.getApiUrl(config.endpoints.subscribe), payload)
    console.log('Response:', response.data)
    // call API with axios
    console.log('Submitting:', payload)
    // reset input if successful
    if (response.status === 200) {
      toast.success("🎉 Subscribed successfully!")
      form.value = {
        email: '',
        subscribed_artists: [],
        notification_methods: [],
        phone_number: '',
        telegram_chat_id: ''
      }
    } else {
      toast.error("❌ Subscription failed!")
    }
  } catch (err) {
    console.error('Error submitting form:', err)
    toast.error("❌ Subscription failed!")
  }
}
</script>

<style>
.input {
  @apply w-full px-4 py-2 bg-gray-800 text-white border border-gray-600 rounded focus:outline-none focus:ring-2 focus:ring-green-400;
}
</style>
