<template>
  <v-card class="teal lighten-5 font-weight-bold outline-card" raised outlined>
    <div>{{ title }}</div>
    <v-card class="ma-5" outlined>
      <v-card-text class="outline-card-text">
        <slot />
      </v-card-text>
    </v-card>
  </v-card>
</template>

<script>
export default {
    props: {
        title: String,
    }
}
</script>


<style lang="scss" scoped>
.outline-card {
  height: 100%;
}
</style>