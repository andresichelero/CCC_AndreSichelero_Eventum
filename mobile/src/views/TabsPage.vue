<template>
  <ion-page>
    <ion-tabs>
      <ion-router-outlet></ion-router-outlet>
      <ion-tab-bar slot="bottom">
        <ion-tab-button tab="home" href="/tabs/home">
          <ion-icon :icon="homeOutline" />
          <ion-label>Início</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="events" href="/tabs/events">
          <ion-icon :icon="calendarOutline" />
          <ion-label>Eventos</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="inscriptions" href="/tabs/inscriptions">
          <ion-icon :icon="ticketOutline" />
          <ion-label>Inscrições</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="schedule" href="/tabs/schedule">
          <ion-icon :icon="timeOutline" />
          <ion-label>Agenda</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="profile" href="/tabs/profile">
          <ion-icon :icon="personOutline" />
          <ion-label>Perfil</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script setup lang="ts">
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage, IonRouterOutlet } from '@ionic/vue';
import { calendarOutline, ticketOutline, timeOutline, personOutline, homeOutline } from 'ionicons/icons';
</script>
