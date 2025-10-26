<template>
  <v-container>
    <v-card class="mb-4">
      <v-card-title class="text-h4">{{ event.title }}</v-card-title>
      <v-card-subtitle
        >Organizado por: {{ event.organizer?.name }}</v-card-subtitle
      >
      <v-card-text>
        <v-row>
          <v-col cols="12" md="8">
            <h4>Descrição</h4>
            <p v-html="event.description"></p>
            <v-divider class="my-4"></v-divider>
            <p>
              <strong>Início:</strong> {{ formatDateTime(event.start_date) }}
            </p>
            <p><strong>Fim:</strong> {{ formatDateTime(event.end_date) }}</p>
          </v-col>
          <v-col cols="12" md="4">
            <!-- Organizer Actions -->
            <v-card v-if="user && event.organizer_id === user.id" class="mb-4">
              <v-card-title>Ações do Organizador</v-card-title>
              <v-card-text>
                <v-btn
                  :to="`/events/${event.id}/edit`"
                  color="primary"
                  block
                  class="mb-2"
                  >Editar Evento</v-btn
                >
                <v-btn
                  :to="`/events/${event.id}/manage-schedule`"
                  color="info"
                  block
                  class="mb-2"
                  >Gerenciar Programação</v-btn
                >
                <v-btn @click="deleteEvent" color="error" block
                  >Remover Evento</v-btn
                >
              </v-card-text>
            </v-card>
            <!-- Participant Inscription -->
            <v-card v-if="user && event.organizer_id !== user.id" class="mb-4">
              <v-card-title>Inscrição</v-card-title>
              <v-card-text>
                <p>
                  <strong>Período de Inscrição:</strong><br />
                  {{ formatDateTime(event.inscription_start_date) }} a
                  {{ formatDateTime(event.inscription_end_date) }}
                </p>
                <v-divider class="my-4"></v-divider>
                <v-btn
                  v-if="isInscriptionOpen && !isInscribed"
                  @click="inscribe"
                  color="primary"
                  block
                  >Inscrever-se</v-btn
                >
                <v-btn
                  v-if="isInscribed"
                  :color="showCancelButton ? 'error' : 'success'"
                  block
                  @mouseover="showCancelButton = true"
                  @mouseleave="showCancelButton = false"
                  @click="showCancelButton ? cancelInscription() : null"
                  >{{
                    showCancelButton
                      ? "Cancelar inscrição"
                      : "Você está inscrito"
                  }}</v-btn
                >
                <v-btn
                  v-if="isInscribed && isEventFinished"
                  @click="downloadCertificate"
                  color="primary"
                  block
                  class="mt-2"
                >
                  Baixar Certificado
                </v-btn>
                <v-btn v-if="!isInscriptionOpen" block disabled
                  >Inscrições Encerradas</v-btn
                >
              </v-card-text>
            </v-card>
            <!-- Speaker Submission -->
            <v-card v-if="user && user.role === 2" class="mb-4">
              <v-card-title>Submissão de Trabalhos</v-card-title>
              <v-card-text>
                <p v-if="event.submission_start_date">
                  <strong>Período de Submissão:</strong><br />
                  {{ formatDateTime(event.submission_start_date) }} a {{ formatDateTime(event.submission_end_date) }}
                </p>
                <v-divider class="my-4"></v-divider>
                <v-btn
                  v-if="isSubmissionOpen"
                  :to="`/events/${event.id}/submit`"
                  color="info"
                  block
                  >Submeter Trabalho</v-btn
                >
                <v-btn v-else block disabled>Submissões Fechadas</v-btn>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Participants List -->
    <v-card v-if="user && event.organizer_id === user.id" class="mb-4">
      <v-card-title
        >Participantes Inscritos ({{
          event.participants?.length || 0
        }})</v-card-title
      >
      <v-card-text>
        <v-btn
          @click="exportParticipants"
          color="secondary"
          size="small"
          class="mb-4"
          >Exportar para CSV</v-btn
        >
        <v-list v-if="event.participants?.length > 0">
          <v-list-item
            v-for="participant in event.participants"
            :key="participant.id"
          >
            {{ participant.name }} ({{ participant.email }})
          </v-list-item>
        </v-list>
        <p v-else>Ainda não há participantes inscritos neste evento.</p>
      </v-card-text>
    </v-card>

    <!-- Submissions List -->
    <v-card v-if="user && event.organizer_id === user.id" class="mb-4">
      <v-card-title
        >Trabalhos Submetidos ({{
          event.submissions?.length || 0
        }})</v-card-title
      >
      <v-card-text>
        <v-card v-for="sub in event.submissions" :key="sub.id" class="mb-2">
          <v-card-title>{{ sub.title }}</v-card-title>
          <v-card-text>
            <p>
              <strong>Autor:</strong> {{ sub.author?.name }} ({{
                sub.author?.email
              }})
            </p>
            <p>
              <strong>Arquivo:</strong>
              <a
                :href="`/api/submissions/${sub.id}/download`"
                target="_blank"
                >{{ sub.file_path }}</a
              >
            </p>
          </v-card-text>
          <v-card-actions>
            <v-chip :color="getStatusColor(sub.status)" size="small">
              {{ getStatusText(sub.status) }}
            </v-chip>
            <v-spacer></v-spacer>
            <v-btn
              @click="evaluateSubmission(sub.id, 3)"
              color="success"
              size="small"
              >Aprovar</v-btn
            >
            <v-btn
              @click="evaluateSubmission(sub.id, 4)"
              color="error"
              size="small"
              class="ml-2"
              >Rejeitar</v-btn
            >
          </v-card-actions>
        </v-card>
        <p v-if="!event.submissions?.length">
          Nenhum trabalho foi submetido a este evento ainda.
        </p>
      </v-card-text>
    </v-card>

    <!-- Quem Vai (Networking) -->
    <v-card v-if="user && isInscribed" class="mb-4">
      <v-card-title>Quem Vai (Networking)</v-card-title>
      <v-card-text>
        <p class="text-caption mb-4">
          Esta lista mostra outros participantes que optaram por
          compartilhar seu perfil publicamente neste evento.
        </p>
        <v-list
          v-if="event.public_participants && event.public_participants.length > 0"
        >
          <v-list-item
            v-for="participant in event.public_participants"
            :key="participant.id"
          >
            <span v-if="participant.id !== user.id">{{
              participant.name
            }}</span>
            <span v-else><strong>{{ participant.name }} (Você)</strong></span>
          </v-list-item>
        </v-list>
        <p v-else>
          Nenhum participante habilitou o perfil público para este evento ainda.
          Você pode habilitar o seu em "Meu Perfil".
        </p>
      </v-card-text>
    </v-card>

    <!-- Schedule -->
    <v-card>
      <v-card-title>Programação</v-card-title>
      <v-card-text>
        <FullCalendar :options="calendarOptions" />
        <p v-if="activities.length === 0">
          A programação deste evento ainda não foi divulgada.
        </p>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";

export default {
  name: "EventDetail",
  components: {
    FullCalendar,
  },
  props: ["id"],
  data() {
    return {
      event: {},
      activities: [],
      isInscriptionOpen: false,
      isSubmissionOpen: false,
      isInscribed: false,
      user: null,
      showCancelButton: false,
      calendarOptions: {
        plugins: [dayGridPlugin, timeGridPlugin],
        initialView: "timeGridWeek",
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek",
        },
        editable: false, // Leitura-apenas
        events: [],
        validRange: {
          start: null,
          end: null,
        },
      },
    };
  },
  computed: {
    isEventFinished() {
      if (this.event && this.event.end_date) {
        return new Date(this.event.end_date) < new Date();
      }
      return false;
    }
  },
  async created() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        const response = await axios.get("/api/");
        if (response.data.authenticated) {
          this.user = response.data.user;
        }
        const eventResponse = await axios.get(`/api/events/${this.id}`);
        this.event = eventResponse.data.event;
        this.activities = eventResponse.data.activities;
        this.isInscriptionOpen = eventResponse.data.is_inscription_open;
        this.isSubmissionOpen = eventResponse.data.is_submission_open;
        this.isInscribed =
          this.user &&
          this.event.participants?.some((p) => p.id === this.user.id);

        // Set valid range for calendar (show only within event period)
        const eventStart = new Date(this.event.start_date);
        const eventEnd = new Date(this.event.end_date);
        this.calendarOptions.validRange.start = eventStart;
        this.calendarOptions.validRange.end = eventEnd;

        // Mapeia as atividades para o formato do FullCalendar
        this.calendarOptions.events = this.activities.map((act) => ({
          id: act.id,
          title: act.title,
          start: act.start_time,
          end: act.end_time,
          description: act.description, // Podemos usar isso em popups futuros
          location: act.location,
        }));
      } catch (err) {
        console.error(err);
      }
    },
    formatDateTime(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString("pt-BR");
    },
    async inscribe() {
      try {
        await axios.post(`/api/events/${this.id}/inscribe`);
        await this.loadData();
      } catch (err) {
        console.error(err);
      }
    },
    async cancelInscription() {
      try {
        await axios.delete(`/api/events/${this.id}/inscribe`);
        await this.loadData();
      } catch (err) {
        console.error(err);
      }
    },
    async deleteEvent() {
      if (confirm("Tem certeza que deseja remover este evento?")) {
        try {
          await axios.delete(`/api/events/${this.id}`);
          this.$router.push("/dashboard");
        } catch (err) {
          console.error(err);
        }
      }
    },
    async downloadCertificate() {
      try {
        // Abre o link da API em uma nova aba; o backend forçará o download.
        window.open(`/api/events/${this.event.id}/certificate`, "_blank");
        await this.loadData();
      } catch (err) {
        console.error(err);
      }
    },
    async exportParticipants() {
      try {
        // Trigger download
        window.open(`/api/events/${this.event.id}/export_participants`, "_blank");
      } catch (err) {
        console.error(err);
      }
    },
    async evaluateSubmission(subId, status) {
      const allowedStatuses = [3, 4]; // 3: Aprovar, 4: Rejeitar
      if (!allowedStatuses.includes(status)) {
        console.error("Status inválido para avaliação de submissão:", status);
        return;
      }
      try {
        await axios.post(`/api/submissions/${subId}/evaluate`, {
          new_status: status,
        });
        await this.loadData();
      } catch (err) {
        console.error(err);
      }
    },
    getStatusColor(status) {
      switch (status) {
        case 1:
          return "info";
        case 3:
          return "success";
        case 4:
          return "error";
        default:
          return "default";
      }
    },
    getStatusText(status) {
      switch (status) {
        case 1:
          return "Submetido";
        case 3:
          return "Aprovado";
        case 4:
          return "Rejeitado";
        default:
          return "Em avaliação";
      }
    },
  },
};
</script>

<style scoped>
.v-card {
  margin-bottom: 20px;
}

.v-card-title {
  font-size: 1.5rem;
  font-weight: 500;
}

.v-card-subtitle {
  font-size: 1rem;
  color: #666;
}

.v-card-text {
  padding: 16px;
}

.v-divider {
  margin: 16px 0;
}

.v-btn {
  text-transform: none;
}

.v-list-item {
  padding: 12px 16px;
}

.v-list-item-title {
  font-weight: 500;
}

.v-list-item-subtitle {
  font-size: 0.875rem;
  color: #666;
}

.v-chip {
  font-size: 0.875rem;
  font-weight: 500;
}

.fc-header-toolbar {
  justify-content: center !important;
}
</style>