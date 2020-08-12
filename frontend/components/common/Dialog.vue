<template>
  <v-dialog v-model="dialog" :max-width="width">
    <slot />
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
    };
  },

  props: {
    width: Number,
  },

  methods: {
    open() {
      this.dialog = true;
    },

    close() {
      this.dialog = false;
    },
  },
};
</script>