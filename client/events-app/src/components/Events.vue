<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useEventsStore } from '../stores/events.js'
import { event } from 'quasar'

const eventData = ref({
    id: -1,
    name: "",
    description: "",
    start_date: "",
    start_time: "",
    end_date: "",
    end_time: "",
    repeats: false,
    repeat_types: {},
})

const eventsList = ref([])
const isNewEvent = ref(false)


function newEvent() {
    eventData.value = {
        id: -1,
        name: "",
        description: "",
        start_date: "",
        start_time: "",
        end_date: "",
        end_time: "",
        repeats: false,
    }
    isNewEvent.value = true
}

async function saveEvent() {
    const eventsStore = useEventsStore()
    const workingId = eventData.value.id
    console.log(workingId)
    const newEvent = {
        name: eventData.value.name,
        description: eventData.value.description,
        start_time: `${eventData.value.start_date}T${eventData.value.start_time}`, //Not ideal, but it works
        end_time: `${eventData.value.end_date}T${eventData.value.end_time}`, //Not ideal but it works
        repeats: eventData.value.repeats,
    }
    if (isNewEvent.value) {
        const responseObject = await eventsStore.addEvent(newEvent)
        if (responseObject) {
            // Add the new event to the list just id and name
            eventsList.value = eventsStore.getEventListItems
        }
    }
    else if (!isNewEvent.value) {
        const updatedEvent = await eventsStore.updateEvent(workingId, newEvent)
        eventsList.value = eventsStore.getEventListItems
    }
    isNewEvent.value = false
}

async function deleteEvent() {
    const eventsStore = useEventsStore()
    const success = await eventsStore.deleteEvent(eventData.value.id) 
    if (success) {
        eventsList.value = eventsList.value.filter((event) => event.name !== eventData.value.name)
    }
}

function getEventById(id) {
    const eventsStore = useEventsStore()
    const event = eventsStore.getById(id)
    eventData.value = {
        id: event.id,
        name: event.name,
        description: event.description,
        // Get just the date part of the start_time
        start_date: event.start_time.split("T")[0],
        // Get just the time part of the start_time
        start_time: event.start_time.split("T")[1].split(".")[0],
        // Get just the date part of the end_time
        end_date: event.end_time.split("T")[0],
        // Get just the time part of the end_time
        end_time: event.end_time.split("T")[1].split(".")[0],
        repeats: event.repeats,
    }
}

function updateEventRef(newEvent) {
    eventData.value = {
        id: newEvent.id,
        name: newEvent.name,
        description: newEvent.description,
        // Get just the date part of the start_time
        start_date: newEvent.start_time.split("T")[0],
        // Get just the time part of the start_time
        start_time: newEvent.start_time.split("T")[1].split(".")[0],
        // Get just the date part of the end_time
        end_date: newEvent.end_time.split("T")[0],
        // Get just the time part of the end_time
        end_time: newEvent.end_time.split("T")[1].split(".")[0],
        repeats: newEvent.repeats,
    }
}

onMounted(async () => {
    const eventsStore = useEventsStore()
    await eventsStore.fetchEvents()
    if (eventsStore.events.length > 0) {        
        console.log("Got Events")
        updateEventRef(eventsStore.events[0])
        eventsList.value = eventsStore.events
        console.log(eventData.value)
    }
    else {
        console.log("No Events")
    }

})
</script>

<template>
    <div class="event-container">
        <div>
            <q-list>
                <q-item v-for="event in eventsList" :key="event.id" v-model="eventData.name" clickable @click="getEventById(event.id)">
                    <q-item-section>
                        <q-item-label>{{ event.name }}</q-item-label>
                    </q-item-section>
                </q-item>
            </q-list>
            <q-btn label="New" color="primary" @click="newEvent"/>
        </div>
        <div class="event-fields">
            <q-input label="Event Name" v-model="eventData.name"/>
            <q-input label="Event Description" v-model="eventData.description" />
            <q-checkbox v-model="eventData.repeats" label="Repeatable" />
            <q-btn label="Save" color="primary" @click="saveEvent()"/>
            <q-btn label="Delete" color="negative" @click="deleteEvent(eventData.id)"/>
        </div>
        <div class="datetime-container">
            <p>Start Date and Time</p>
            <q-date v-model="eventData.start_date" mask="YYYY-MM-DD" color="blue" label="Start Date"  />
            <q-time v-model="eventData.start_time" mask="HH:mm:ss" color="blue" label="Start Time"/>
        </div>
        <div class = "datetime-container">
            <p>End Date and Time</p>
            <q-date v-model="eventData.end_date" mask="YYYY-MM-DD" color="blue" label="End Date" />
            <q-time v-model="eventData.end_time" mask="HH:mm:ss" color="blue" label="End Time"/>
        </div>
    </div>
</template>

<style scoped>
.event-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: fit-content;
    width: 100vw;
    min-height: 50vh;
}

.event-container text {
    min-width: 10vw;
    min-height: 10vh;
    font-size: 1.5rem;
}

.q-date {
    background-color: var(--q-background-color);
}

.q-time {
    background-color: var(--q-background-color);
}

.event-fields {
    display: flex;
    flex-direction: column;
    justify-content: left;
    align-items: left;
    margin-left: 2rem;
    margin-right: 2rem;
    height: fit-content;
    gap: 2rem;
    min-height: 30vh;
}

.datetime-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-left: 2rem;
    margin-right: 2rem;
    height: fit-content;
    gap: 2rem;
    min-height: 30vh;
}
</style>