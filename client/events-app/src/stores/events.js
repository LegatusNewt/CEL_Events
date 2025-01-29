import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { format } from 'quasar';

const server_url = 'http://localhost:5000'
const events_url = `${server_url}/events`

export const useEventsStore = defineStore('events', {
    state: () => ({
        events: ref([]),
        schedule: ref([]),
        selectedDates: ref([]),
    }),
    getters: {
        getEvents(state) {
            return state.events
        },
        getSchedule(state) {
            return state.schedule
        },
        getSelectedDates(state) {
            return state.selectedDates
        },
        getEventListItems(state) {
            return state.events.map(event => {
                return {
                    name: event.name,
                    id: event.id,
                }
            })
        },
        getById: (state) => (id) => {
            return state.events.find(event => event.id === id)
        },
        getAgendaEvents(state) {
            const formattedEvents = {}
            for (const event of state.schedule) {
                const date = new Date(event.start_time)
                date.setHours(0, 0, 0, 0)
                // Date key is just iso string without time
                const dateKey = date.toISOString().split('T')[0]
                if (!formattedEvents[dateKey]) {
                    formattedEvents[dateKey] = []
                }
                let showEvent = {
                    id: event.id,
                    title: event.name,
                    start: event.start_time,
                    end: event.end_time,
                }
                formattedEvents[dateKey].push(showEvent)
            }
            return formattedEvents
        }
    },
    actions: {
        async addEvent(event) {
            try {
                const response = await fetch(events_url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(event)
                })
                if (!response.ok) {
                    throw new Error('Failed to add event')
                }
                this.fetchEvents()
                return response.json() // Return json of new event
            }
            catch (error) {
                console.error(error)
            }
        },
        async deleteEvent(id) {
            try {
                const response = await fetch(`${events_url}/${id}`, {
                    method: 'DELETE'
                })
                if (!response.ok) {
                    throw new Error('Failed to delete event')
                }
                this.fetchEvents()
                // If doesn't fail we assume it succeeded
                return true;
            }
            catch (error) {
                console.error(error)
            }
        },
        async updateEvent(id, event) {
            try {
                const response = await fetch(`${events_url}/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(event)
                })
                if (!response.ok) {
                    throw new Error('Failed to update event')
                }
                this.fetchEvents()
                return response.json() // Return json of updated event
            }
            catch (error) {
                console.error(error)
            }
        },
        async fetchSchedule() {
            try {
                // Convert start and end to ISOformat
                const start = this.selectedDates[0]
                const end = this.selectedDates[1]

                const response = await fetch(`${events_url}/schedule?start_date=${start}&end_date=${end}`)
                if (!response.ok) {
                    throw new Error('Failed to fetch schedule')
                }
                const data = await response.json()
                this.schedule = data
            }
            catch (error) {
                console.error(error)
            }
        },
        async fetchEvents() {
            try {
                const response = await fetch(events_url)
                if (!response.ok) {
                    throw new Error('Failed to fetch events')
                }
                const data = await response.json()
                this.events = data
            }
            catch (error) {
                console.error(error)
            }
        }
    }
});