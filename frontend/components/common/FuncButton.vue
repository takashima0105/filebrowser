<template>
  <v-btn :color="color" @click="clickFunc" :text="textonly">{{ text }}</v-btn>
</template>

<script>
export default {
  props: {
    color: String,
    clickFunc: Function,
    text: String,
    textonly: Boolean,
  },
};
</script>

