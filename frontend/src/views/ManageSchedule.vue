<template>
  <v-container>
    <v-card class="mb-4">
      <v-card-title class="text-h4">Gerenciar Programação</v-card-title>
      <v-card-subtitle>Evento: {{ event.title }}</v-card-subtitle>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <h5>
              {{ editing ? "Editar Atividade" : "Adicionar Nova Atividade" }}
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
              <v-textarea
                v-model="form.description"
                label="Descrição"
                rows="3"
              ></v-textarea>
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
              <v-text-field
                v-model="form.location"
                label="Local"
                required
              ></v-text-field>
              <v-btn @click="addActivity" color="primary" block>{{
                editing ? "Salvar Alterações" : "Salvar Atividade"
              }}</v-btn>
              <v-btn
                v-if="editing"
                @click="cancelEdit"
                color="secondary"
                block
                class="mt-2"
                >Cancelar</v-btn
              >
              <v-btn
                v-if="editing"
                @click="deleteActivity()"
                color="error"
                block
                class="mt-2"
                >Remover Atividade</v-btn
              >

              <v-divider v-if="editing" class="my-4"></v-divider>
              <div v-if="editing && currentActivity">
                <h5>Controle de Presença</h5>
                
                <div v-if="currentActivity.check_in_open">
                  <p class="text-h4 text-center my-2">{{ currentActivity.check_in_code }}</p>
                  <p class="text-caption text-center">
                    Instrua os participantes a usarem este código para o check-in.
                  </p>
                  <v-btn @click="closeCheckin(currentActivity.id)" color="warning" block>Encerrar Check-in</v-btn>
                </div>
                
                <div v-else>
                  <p class="text-caption">
                    Abra o check-in para gerar um código e permitir a entrada dos participantes.
                  </p>
                  <v-btn @click="openCheckin(currentActivity.id)" color="success" block>Abrir Check-in</v-btn>
                </div>
                
                <p class="text-body-2 mt-4">
                  Participantes Registrados: {{ currentActivity.attendees_count || 0 }}
                </p>
              </div>
            </div>
            <v-alert v-if="error" type="error" class="mt-4">{{
              error
            }}</v-alert>
            <v-alert v-if="message" type="success" class="mt-4">{{
              message
            }}</v-alert>
          </v-col>
          <v-col cols="12" md="8">
            <h5>Programação Atual (Arraste para alterar o horário)</h5>
            <FullCalendar :options="calendarOptions" />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title>
        <span class="text-h5">Calendário</span>
      </v-card-title>
      <v-card-text>
        <full-calendar
          :options="calendarOptions"
          @eventDrop="handleActivityDrop"
          @eventClick="handleEventClick"
        />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";
// --- Adição Início ---
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
// --- Adição Fim ---

export default {
  name: "ManageSchedule",
  components: {
    FullCalendar,
  },
  props: ["id"],
  data() {
    return {
      event: {},
      activities: [], // Manteremos isso para referência, mas o calendário usará 'calendarOptions'
      form: {
        title: "",
        description: "",
        start_time: "",
        end_time: "",
        location: "",
      },
      editing: false,
      editingId: null,
      error: "",
      message: "",
      currentActivity: null, // Armazena o objeto completo da atividade em edição
      calendarOptions: {
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        initialView: "timeGridWeek",
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,timeGridDay",
        },
        editable: true,
        eventDrop: this.handleActivityDrop,
        eventClick: this.handleEventClick,
        events: [], // Será preenchido pelo loadData
      },
    };
  },
  async created() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        const response = await axios.get(`/api/events/${this.id}`)
        this.event = response.data.event
        this.activities = response.data.activities
        
        const now = new Date()
        const eventStart = new Date(this.event.start_date)
        const eventEnd = new Date(this.event.end_date)
        this.calendarOptions.validRange = {
          start: eventStart > now ? eventStart : now,
          end: eventEnd
        }
        
        // Mapeia as atividades para o formato do FullCalendar
        this.calendarOptions.events = this.activities.map(act => ({
          id: act.id,
          title: act.title,
          start: act.start_time,
          end: act.end_time,
          extendedProps: act // Armazena o objeto original
        }))
        
        // Se estávamos editando, atualiza os dados da atividade atual
        if (this.editing && this.editingId) {
          this.currentActivity = this.activities.find(a => a.id === this.editingId)
        }
      } catch (err) {
        console.error(err)
      }
    },
    formatDateTime(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString("pt-BR");
    },
    formatTime(dateString) {
      const date = new Date(dateString);
      return date.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    async addActivity() {
      const data = { ...this.form };
      this.error = "";
      this.message = "";

      if (!data.title || !data.start_time || !data.end_time || !data.location) {
        this.error = "Por favor, preencha todos os campos obrigatórios.";
        return;
      }

      try {
        data.start_time =
          data.start_time.length === 16
            ? data.start_time + ":00"
            : data.start_time;
        data.end_time =
          data.end_time.length === 16 ? data.end_time + ":00" : data.end_time;
      } catch (e) {
        this.error = "Data/hora inválida.";
        return;
      }

      try {
        if (this.editing) {
          await axios.put(`/api/activities/${this.editingId}`, data);
          this.message = "Atividade atualizada com sucesso!";
        } else {
          await axios.post(`/api/events/${this.id}/activities`, data);
          this.message = "Atividade adicionada com sucesso!";
        }
        this.resetForm(); // Função helper extraída
        await this.loadData(); // Recarrega os eventos do calendário
      } catch (err) {
        this.error = err.response?.data?.error || "Erro ao salvar atividade.";
      }
    },
    handleEventClick(clickInfo) {
      // Preenche o formulário ao clicar em um evento
      const act = clickInfo.event.extendedProps;
      this.form = {
        title: act.title,
        description: act.description,
        start_time: new Date(act.start_time).toISOString().slice(0, 16),
        end_time: new Date(act.end_time).toISOString().slice(0, 16),
        location: act.location,
      };
      this.editing = true;
      this.editingId = act.id;
      this.currentActivity = act;
      this.message = "";
      this.error = "";
    },
    async handleActivityDrop(dropInfo) {
      // Manipula o 'arrastar e soltar' 
      this.message = 'Atualizando atividade...'
      this.error = ''
      
      const activityId = dropInfo.event.id
      const data = {
        start_time: this.toLocalISOString(dropInfo.event.start),
        end_time: this.toLocalISOString(dropInfo.event.end)
      }

      try {
        await axios.put(`/api/activities/${activityId}`, data)
        this.message = 'Horário da atividade atualizado com sucesso!'
        await this.loadData()
      } catch (err) {
        this.error = err.response?.data?.error || 'Erro ao atualizar horário.'
        dropInfo.revert() // Reverte a mudança no calendário em caso de erro
      }
    },
    async deleteActivity(activityId) {
      // Se 'activityId' não for passado, tenta pegar do formulário
      const idToDelete = activityId || this.editingId;
      if (!idToDelete) return;

      if (confirm("Tem certeza que deseja remover esta atividade?")) {
        try {
          await axios.delete(`/api/activities/${idToDelete}`);
          await this.loadData();
          this.resetForm();
        } catch (err) {
          console.error(err);
        }
      }
    },
    resetForm() {
      this.form = {
        title: "",
        description: "",
        start_time: "",
        end_time: "",
        location: "",
      };
      this.editing = false;
      this.editingId = null;
      this.currentActivity = null;
      this.error = "";
      this.message = "";
    },
    cancelEdit() {
      this.resetForm();
    },
    // Métodos de Check-in
    async openCheckin(activityId) {
      this.error = ''
      this.message = ''
      try {
        await axios.post(`/api/activities/${activityId}/open-checkin`)
        this.message = 'Check-in aberto!'
        await this.loadData() // Recarrega os dados da atividade (código, status)
      } catch (err) {
        this.error = err.response?.data?.error || 'Erro ao abrir check-in.'
      }
    },
    async closeCheckin(activityId) {
      this.error = ''
      this.message = ''
      try {
        await axios.post(`/api/activities/${activityId}/close-checkin`)
        this.message = 'Check-in encerrado!'
        await this.loadData() // Recarrega os dados da atividade
      } catch (err) {
        this.error = err.response?.data?.error || 'Erro ao fechar check-in.'
      }
    },
    toLocalISOString(date) {
      const tzOffset = date.getTimezoneOffset() * 60000 // offset in milliseconds
      const localISOTime = new Date(date.getTime() - tzOffset).toISOString().slice(0, -1)
      return localISOTime
    }
  },
};
</script>

<style scoped>
.fc-header-toolbar {
  justify-content: center !important;
}
</style>