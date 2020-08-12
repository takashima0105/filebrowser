<template>
  <v-app-bar color="orange" elevation="0" dark app flat clipped-right>
    <v-toolbar-title>SiteManagement</v-toolbar-title>
    <v-spacer />
    <div class="pa-2">
      <v-btn block class="blue white--text" @click="logout">LogOut</v-btn>
    </div>
    <v-menu left bottom offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon v-bind="attrs" v-on="on">
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item :to="{name: 'config'}">
          <v-list-item-title>システム設定</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-title>お問い合わせ</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <template v-slot:extension>
      <template v-for="(link, index) in links">
        <LinkButton
          v-bind:key="index"
          :link="link.url"
          :text="link.text"
          :color="link.color"
          :icon="link.icon"
          :textonly="link.textonly"
          :exact="link.exact"
          :disabled="link.disabled"
        ></LinkButton>
      </template>
    </template>
  </v-app-bar>
</template>

<script>
import LinkButton from "~/components/common/LinkButton.vue";

export default {
  props: {
    links: Array,
  },

  components: {
    LinkButton: LinkButton,
  },

  methods: {
    // logout処理
    logout() {
      this.$auth.logout();
    },
  },
};
</script>