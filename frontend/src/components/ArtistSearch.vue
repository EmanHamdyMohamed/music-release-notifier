<template>
  <div class="relative w-full">
    <!-- Selected items display -->
    <div v-if="selectedItems.length > 0" class="flex flex-wrap gap-2 mb-2">
      <span v-for="(item, index) in selectedItems" :key="item.id"
        class="inline-flex items-center bg-gray-200 rounded-full px-3 py-1 text-sm font-medium text-gray-700">
        <img v-if="item.image_url" :src="item.image_url" :alt="item.name" class="w-5 h-5 rounded-full mr-2 object-cover">
        {{ item.name }}
        <button @click="removeItem(index)" class="ml-2 text-gray-500 hover:text-gray-700 focus:outline-none"
          aria-label="Remove item">
          &times;
        </button>
      </span>
    </div>

    <!-- Search input -->
    <div class="relative">
      <input type="text" v-model="searchQuery" @input="onSearchInput" @focus="showDropdown = true" @blur="handleBlur"
        :placeholder="placeholder" class="input" />
      <div v-if="isLoading" class="absolute inset-y-0 right-0 flex items-center pr-3">
        <svg class="animate-spin h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
          viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
          </path>
        </svg>
      </div>
    </div>

    <!-- Dropdown with search results -->
    <div v-if="showDropdown && (searchResults.length > 0 || isLoading)"
      class="absolute z-10 mt-1 w-full bg-black shadow-lg rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm max-h-60">
      <div v-for="item in searchResults" :key="item.id" @mousedown="toggleItem(item)" :class="{
        'bg-gray-700': isSelected(item),
        'text-gray-900': !isSelected(item),
      }" class="cursor-default select-none relative py-2 pl-3 pr-9 hover:bg-gray-700">
        <div class="flex justify-start mb-3">
          <!-- Image thumbnail -->
          <img v-if="item.image_url" :src="item.image_url" :alt="item.name" width="30" height="30"
            class="rounded-full object-cover">
          <!-- Fallback avatar if no image -->
          <div v-else
            class="flex-shrink-0 h-6 w-6 rounded-full bg-gray-300 flex items-center justify-center text-gray-500 text-xs font-medium mr-3">
            {{ item.name.charAt(0).toUpperCase() }}
          </div>

          <div class="min-w-0">
            <span class="text-lg font-semibold text-white mx-2">
              {{ item.name }}
            </span>
            <!-- Optional secondary text -->
            <p v-if="item.secondaryText" class="text-xs text-gray-500 truncate">
              {{ item.secondaryText }}
            </p>
          </div>

          <span v-if="isSelected(item)" class="ml-2 text-blue-600">
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd" />
            </svg>
          </span>
        </div>
      </div>
      <div v-if="isLoading" class="px-4 py-2 text-gray-500 italic">Loading...</div>
      <div v-if="!isLoading && searchResults.length === 0 && searchQuery.length >= minSearchChars"
        class="px-4 py-2 text-gray-500">
        No results found
      </div>
    </div>
  </div>
</template>

<script setup>
import { debounce } from 'lodash';
import axios from 'axios'
import { ref, watch, onMounted } from 'vue'
import config from '../config.js'

// Props
const props = defineProps({
  initialSelected: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: 'Search...'
  },
  minSearchChars: {
    type: Number,
    default: 2
  }
})

// Emits
const emit = defineEmits(['update:selected', 'change', 'search-error'])

// State
const searchQuery = ref('')
const searchResults = ref([])
const selectedItems = ref([])
const showDropdown = ref(true)
const isLoading = ref(false)
const debouncedSearch = ref(null)

// Computed
const isSelected = (item) => {
  return selectedItems.value.some(selected => selected.id === item.id)
}

// Methods
const onSearchInput = () => {
  if (searchQuery.value.trim().length < props.minSearchChars) {
    searchResults.value = []
    return
  }
  debouncedSearch.value()
}

const performSearch = async () => {
  isLoading.value = true
  showDropdown.value = true

  try {
    const response = await axios.get(config.getApiUrl(config.endpoints.searchArtists), {
      params: { q: searchQuery.value }
    })

    if (response.status !== 200) {
      throw new Error(`API request failed with status ${response.status}`)
    }

    const results = response.data?.artists || []
    searchResults.value = results.map(item => ({
      id: item.id,
      name: item.name,
      image_url: item.image_url,
      raw: item,
      url: item.url
    }))

  } catch (error) {
    console.error('Search failed:', error)
    searchResults.value = []
    emit('search-error', error)
  } finally {
    isLoading.value = false
  }
}

const toggleItem = (item) => {
  const index = selectedItems.value.findIndex(selected => selected.id === item.id)

  if (index === -1) {
    selectedItems.value.push(item)
  } else {
    selectedItems.value.splice(index, 1)
  }

  emit('update:selected', selectedItems.value)

}

const removeItem = (index) => {
  selectedItems.value.splice(index, 1)
  emit('update:selected', selectedItems.value)
  emit('change', selectedItems.value)
}

const handleBlur = () => {
  setTimeout(() => {
    showDropdown.value = false
  }, 200)
}

const clearSearch = () => {
  searchQuery.value = ''
  searchResults.value = []
  showDropdown.value = false
}

// Lifecycle
onMounted(() => {
  selectedItems.value = [...props.initialSelected]
  debouncedSearch.value = debounce(performSearch, 300)
})

// Watchers
watch(() => props.initialSelected, (newVal) => {
  selectedItems.value = [...newVal]
})

</script>

<style scoped></style>