<script setup>
//import quasar calendar
import { QCalendarAgenda, today } from '@quasar/quasar-ui-qcalendar'
import '@quasar/quasar-ui-qcalendar/index.css'
import {ref, onMounted } from 'vue'
import { useEventsStore } from '../stores/events.js'

const reset = {}
const selectedDate = ref(today())
const calendar = ref()
const formattedEvents = ref(reset)

function onNext() {
    if (calendar.value) {
        calendar.value.next()
        selectedDate.value = calendar.value.value
    }
}

function onPrev() {
    if (calendar.value) {
        calendar.value.prev()
        selectedDate.value = calendar.value.value
    }
}

function onToday() {
    if (calendar.value) {
        calendar.value.value = today()
        selectedDate.value = calendar.value.value
    }
}

async function onChange({start, end}) {
    resetFormattedEvents()
    const eventsStore = useEventsStore()
    eventsStore.selectedDates = [start, end]
    await eventsStore.fetchSchedule()
    formattedEvents.value = formatEvents()
}

function resetFormattedEvents() {
    for (const key in formattedEvents) {
        console.log(key)
        //delete formattedEvents[key]
    }
}

function formatEvents() {
    // Format events for QCalendar from API data
    const eventsStore = useEventsStore()

    for (const event of eventsStore.schedule) {
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
}

function getFormattedEvents(day) {
    // Get formatted events
    const eventsStore = useEventsStore()
    const events = eventsStore.getAgendaEvents
    // Date key is just iso string without time
    const dateKey = day.date
    const dayEvents = events[dateKey] || []
    return dayEvents
}

onMounted(async () => {
    // Get Events data from API
    resetFormattedEvents()
    const eventsStore = useEventsStore()
    await eventsStore.fetchSchedule()
    formattedEvents.value = formatEvents()
})

</script>

<template>
    <div class="calendar-container">
        <div>
            <text h5>Events Calendar</text>
            <div>
                <text>{{ selectedDate }}</text>
            </div>
            <q-btn @click="onPrev" label="Prev" />            
            <q-btn @click="onToday" label="Today" />
            <q-btn @click="onNext" label="Next" />
        </div>
        <q-calendar-agenda 
            ref="calendar"
            v-model="selectedDate"
            view="week"
            dark
            :left-column-options="leftColumnOptions"
            :right-column-options="rightColumnOptions"
            column-options-id="id"
            column-options-label="label"
            :day-min-height="200"
            animated
            bordered
            @change="onChange"
            @moved="onMoved"
            @click-date="onClickDate"
        >
            <template #day="{ scope: { timestamp } }">
                <template v-for="event in getFormattedEvents(timestamp)" :key="event.id">
                    <div>
                        <q-card>
                            <q-card-section class="bg-primary text-white">
                                <q-badge :label="event.title" />
                                <text>{{ event.start }}</text>
                                <text>{{ event.end }}</text>
                            </q-card-section>                            
                        </q-card>
                    </div>
                </template>
            </template>
        </q-calendar-agenda>
    </div>
</template>

<style scoped>
.calendar-container {
    height: fit-content;
    width: 100vw;
    margin-bottom: 5rem;
}
.q-calendar-agenda {
    height: fit-content;
    width: 100vw;
}
</style>
