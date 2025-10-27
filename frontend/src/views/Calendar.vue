<template>
  <div class="calendar-section">
    <v-container>
      <v-card class="elevation-4" color="rgba(255,255,255,0.95)">
        <v-card-title class="text-h4 primary--text font-weight-bold">
          <v-icon size="32" class="me-2">mdi-calendar</v-icon>
          Calendário de Eventos
        </v-card-title>
        <v-card-text>
          <FullCalendar :options="calendarOptions" />
        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

export default {
  name: 'Calendar',
  components: {
    FullCalendar,
  },
  data() {
    return {
      calendarOptions: {
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        initialView: 'dayGridMonth',
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay',
        },
        editable: false,
        eventClick: this.handleEventClick,
        events: [],
        height: 600,
        slotMinTime: '00:00:00',
        slotMaxTime: '23:59:00',
        eventDisplay: 'block',
        eventTimeFormat: {
          hour: '2-digit',
          minute: '2-digit',
          meridiem: false,
        },
      },
    };
  },
  async created() {
    await this.loadCalendarData();
  },
  methods: {
    async loadCalendarData() {
      try {
        const response = await axios.get('/api/calendar');
        const calendarItems = response.data.calendar_items;

        // Mapeia os itens do calendário para o formato do FullCalendar
        this.calendarOptions.events = calendarItems.map((item) => ({
          id: item.id,
          title: item.title,
          start: item.start,
          end: item.end,
          backgroundColor: item.type === 'event' ? '#1976D2' : '#FF9800',
          borderColor: item.type === 'event' ? '#0D47A1' : '#E65100',
          textColor: '#FFFFFF',
          extendedProps: item,
        }));
      } catch (err) {
        console.error('Erro ao carregar dados do calendário:', err);
      }
    },
    handleEventClick(clickInfo) {
      const item = clickInfo.event.extendedProps;
      if (item.type === 'event') {
        // Redireciona para a página do evento
        this.$router.push(`/events/${item.id.split('_')[1]}`);
      } else if (item.type === 'activity') {
        // Para atividades, também redireciona para o evento
        // Como não temos o event_id na atividade, podemos buscar ou redirecionar para eventos
        this.$router.push('/events');
      }
    },
  },
};
</script>

<style scoped>
.calendar-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 2rem 0 20px 0;
}

@media (max-width: 600px) {
  .calendar-section {
    padding: 2rem 10px 10px 10px;
  }
}
</style>
