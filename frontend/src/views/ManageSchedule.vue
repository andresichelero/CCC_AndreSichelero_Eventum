<template>
  <div class="manage-schedule-section">
    <v-container>
    <v-card class="mb-4">
      <v-card-title class="text-h4">Gerenciar Programação</v-card-title>
      <v-card-subtitle>Evento: {{ event.title }}</v-card-subtitle>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <h5>
              {{ editing ? 'Editar Atividade' : 'Adicionar Nova Atividade' }}
            </h5>
            <p>
              <strong>Período do Evento:</strong>
              {{ formatDateTime(event.start_date) }} até
              {{ formatDateTime(event.end_date) }}
            </p>
            <div>
              <v-text-field
                v-model="form.title"
                label="Título da Atividade"
                required
              ></v-text-field>
              <v-textarea v-model="form.description" label="Descrição" rows="3"></v-textarea>
              <v-text-field
                v-model="form.start_time"
                type="datetime-local"
                label="Horário de Início"
                required
              ></v-text-field>
              <v-text-field
                v-model="form.end_time"
                type="datetime-local"
                label="Horário de Fim"
                required
              ></v-text-field>
              <v-text-field v-model="form.location" label="Local" required></v-text-field>
              <v-btn @click="addActivity" color="primary" block>{{
                editing ? 'Salvar Alterações' : 'Salvar Atividade'
              }}</v-btn>
              <v-btn v-if="editing" @click="cancelEdit" color="secondary" block class="mt-2"
                >Cancelar</v-btn
              >
              <v-btn v-if="editing" @click="deleteActivity()" color="error" block class="mt-2"
                >Remover Atividade</v-btn
              >

              <v-divider v-if="editing" class="my-4"></v-divider>
            </div>
            <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
            <v-alert v-if="message" type="success" class="mt-4">{{ message }}</v-alert>
          </v-col>
          <v-col cols="12" md="8">
            <h5>Programação Atual (Arraste para alterar o horário)</h5>
            <FullCalendar v-if="event.start_date" :options="calendarOptions" />
            <div v-else class="text-center py-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
              <p class="mt-2">Carregando programação...</p>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title>
        <span class="text-h5">Calendário</span>
        <v-spacer></v-spacer>
        <v-btn icon @click="showCalendar = !showCalendar">
          <v-icon>{{ showCalendar ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text v-if="showCalendar">
        <full-calendar
          :options="calendarOptions"
          @eventDrop="handleActivityDrop"
          @eventClick="handleEventClick"
        />
      </v-card-text>
    </v-card>
  </v-container>
  </div>
</template>

<script>
import axios from 'axios';
// --- Adição Início ---
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
// --- Adição Fim ---

export default {
  name: 'ManageSchedule',
  components: {
    FullCalendar,
  },
  props: ['id'],
  data() {
    return {
      event: {},
      activities: [], // Manteremos isso para referência, mas o calendário usará 'calendarOptions'
      form: {
        title: '',
        description: '',
        start_time: '',
        end_time: '',
        location: '',
      },
      editing: false,
      editingId: null,
      error: '',
      message: '',
      currentActivity: null, // Armazena o objeto completo da atividade em edição
      showCalendar: true, // Toggle para mostrar/ocultar o calendário maior
      calendarOptions: {
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        initialView: 'timeGridWeek',
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay',
        },
        editable: true,
        eventDrop: this.handleActivityDrop,
        eventClick: this.handleEventClick,
        events: [], // Será preenchido pelo loadData
        slotMinTime: '00:00:00',
        slotMaxTime: '23:59:00',
        height: 600,
        initialDate: null, // Será definido dinamicamente
        slotLabelFormat: {
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        },
        eventTimeFormat: {
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        },
      },
    };
  },
  async created() {
    await this.loadData();
  },
  watch: {
    event: {
      handler(newEvent) {
        if (newEvent && newEvent.start_date) {
          // Atualiza initialDate quando o evento carrega
          this.calendarOptions.initialDate = newEvent.start_date;
          
          // Calcula a duração e define o initialView
          const eventStart = new Date(newEvent.start_date);
          const eventEnd = new Date(newEvent.end_date);
          const durationMs = eventEnd.getTime() - eventStart.getTime();
          const durationDays = durationMs / (1000 * 60 * 60 * 24);

          if (durationDays <= 1) {
            this.calendarOptions.initialView = 'timeGridDay';
          } else if (durationDays <= 7) {
            this.calendarOptions.initialView = 'timeGridWeek';
          } else {
            this.calendarOptions.initialView = 'dayGridMonth';
          }
        }
      },
      deep: true
    }
  },
  methods: {
    async loadData() {
      try {
        const response = await axios.get(`/api/events/${this.id}`);
        this.event = response.data.event;
        this.activities = response.data.activities;

        const now = new Date();
        const eventStart = new Date(this.event.start_date);
        const eventEnd = new Date(this.event.end_date);
        this.calendarOptions.validRange = {
          start: eventStart > now ? eventStart : now,
          end: eventEnd,
        };

        // Define initialDate como o primeiro dia do evento
        this.calendarOptions.initialDate = this.event.start_date;

        // Calcula a duração do evento em dias
        const durationMs = eventEnd.getTime() - eventStart.getTime();
        const durationDays = durationMs / (1000 * 60 * 60 * 24);

        // Define o initialView baseado na duração
        if (durationDays <= 1) {
          this.calendarOptions.initialView = 'timeGridDay';
        } else if (durationDays <= 7) {
          this.calendarOptions.initialView = 'timeGridWeek';
        } else {
          this.calendarOptions.initialView = 'dayGridMonth';
        }

        // Força re-renderização do calendário com novas opções
        this.$nextTick(() => {
          // Força atualização das opções do calendário
          this.$forceUpdate();
        });

        // Mapeia as atividades para o formato do FullCalendar
        this.calendarOptions.events = this.activities.map((act) => ({
          id: act.id,
          title: act.title,
          start: act.start_time,
          end: act.end_time,
          extendedProps: act, // Armazena o objeto original
        }));

        // Se estávamos editando, atualiza os dados da atividade atual
        if (this.editing && this.editingId) {
          this.currentActivity = this.activities.find((a) => a.id === this.editingId);
        }
      } catch (err) {
        console.error(err);
      }
    },
    formatDateTime(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString('pt-BR');
    },
    formatTime(dateString) {
      const date = new Date(dateString);
      return date.toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit',
      });
    },
    formatDateTimeForInput(dateString) {
      const date = new Date(dateString);
      // Formatar para o formato esperado pelo input datetime-local (YYYY-MM-DDTHH:MM)
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day}T${hours}:${minutes}`;
    },
    async addActivity() {
      const data = { ...this.form };
      this.error = '';
      this.message = '';

      if (!data.title || !data.start_time || !data.end_time || !data.location) {
        this.error = 'Por favor, preencha todos os campos obrigatórios.';
        setTimeout(() => { this.error = ''; }, 10000);
        return;
      }

      try {
        data.start_time = data.start_time.length === 16 ? data.start_time + ':00' : data.start_time;
        data.end_time = data.end_time.length === 16 ? data.end_time + ':00' : data.end_time;
      } catch (e) {
        this.error = 'Data/hora inválida.';
        setTimeout(() => { this.error = ''; }, 10000);
        return;
      }

      try {
        if (this.editing) {
          await axios.put(`/api/activities/${this.editingId}`, data);
          this.message = 'Atividade atualizada com sucesso!';
        } else {
          await axios.post(`/api/events/${this.id}/activities`, data);
          this.message = 'Atividade adicionada com sucesso!';
        }
        setTimeout(() => { this.message = ''; }, 10000);
        this.resetForm(false); // Função helper extraída
        await this.loadData(); // Recarrega os eventos do calendário
      } catch (err) {
        this.error = err.response?.data?.error || 'Erro ao salvar atividade.';
        setTimeout(() => { this.error = ''; }, 10000);
      }
    },
    handleEventClick(clickInfo) {
      // Preenche o formulário ao clicar em um evento
      const act = clickInfo.event.extendedProps;
      this.form = {
        title: act.title,
        description: act.description,
        start_time: this.formatDateTimeForInput(act.start_time),
        end_time: this.formatDateTimeForInput(act.end_time),
        location: act.location,
      };
      this.editing = true;
      this.editingId = act.id;
      this.currentActivity = act;
      this.message = '';
      this.error = '';
    },
    async handleActivityDrop(dropInfo) {
      // Manipula o 'arrastar e soltar'
      this.error = '';

      const activityId = dropInfo.event.id;
      const data = {
        start_time: this.toLocalISOString(dropInfo.event.start),
        end_time: this.toLocalISOString(dropInfo.event.end),
      };

      try {
        await axios.put(`/api/activities/${activityId}`, data);
        this.message = 'Horário da atividade atualizado com sucesso!';
        setTimeout(() => { this.message = ''; }, 10000);
        // Pequeno delay para mostrar a mensagem antes de recarregar
        setTimeout(async () => {
          await this.loadData();
        }, 100);
      } catch (err) {
        this.error = err.response?.data?.error || 'Erro ao atualizar horário.';
        setTimeout(() => { this.error = ''; }, 10000);
        dropInfo.revert(); // Reverte a mudança no calendário em caso de erro
      }
    },
    async deleteActivity(activityId) {
      // Se 'activityId' não for passado, tenta pegar do formulário
      const idToDelete = activityId || this.editingId;
      if (!idToDelete) return;

      if (confirm('Tem certeza que deseja remover esta atividade?')) {
        try {
          await axios.delete(`/api/activities/${idToDelete}`);
          await this.loadData();
          this.resetForm();
        } catch (err) {
          console.error(err);
        }
      }
    },
    resetForm(clearMessages = true) {
      this.form = {
        title: '',
        description: '',
        start_time: '',
        end_time: '',
        location: '',
      };
      this.editing = false;
      this.editingId = null;
      this.currentActivity = null;
      if (clearMessages) {
        this.error = '';
        this.message = '';
      }
    },
    cancelEdit() {
      this.resetForm();
    },
    toLocalISOString(date) {
      const tzOffset = date.getTimezoneOffset() * 60000; // offset in milliseconds
      const localISOTime = new Date(date.getTime() - tzOffset).toISOString().slice(0, -1);
      return localISOTime;
    },
  },
};
</script>

<style scoped>
.manage-schedule-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 2rem 0 20px 0;
}

.fc-header-toolbar {
  justify-content: center !important;
}

@media (max-width: 600px) {
  .manage-schedule-section {
    padding: 2rem 10px 10px 10px;
  }
}
</style>
