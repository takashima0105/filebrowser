<template>
  <v-btn :to="link" :text="textonly" :color="color" rounded :exact="exact" :disabled="disabled">
    <v-icon>{{ icon }}</v-icon>
    <span>{{ text }}</span>
  </v-btn>
</template>

<script>
export default {
  props: {
    link: String,
    text: String,
    textonly: Boolean,
    color: String,
    icon: String,
    exact: Boolean,
    disabled: Boolean,
  },
};
</script>

