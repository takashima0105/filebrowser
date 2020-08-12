<template>
  <v-snackbar v-model="snackbar" timeout="-1" :color="snack_color" top>
    {{ message }}
    <template v-slot:action="{ attrs }">
      <v-btn icon @click="snackbar_close" v-bind="attrs" exact>
        <v-icon>mdi-window-close</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      snackbar: false,
    };
  },

  props: {
    message: String,
    snack_color: String,
    snackbar_close: Function,
  },

  methods: {
    open() {
      this.snackbar = true;
    },

    close() {
      this.snackbar = false;
    },
  },

  watch: {
    timeout: function () {
      setTimeout(() => {}, this.timeout);
    },
  },
};
</script>