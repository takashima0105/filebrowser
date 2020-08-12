<template>
  <v-hover v-slot:default="{ hover }">
    <v-card
      class="teal lighten-5"
      :elevation="hover ? 6 : 2"
      :class="{ 'on-hover': hover }"
      min-width="150px"
    >
      <v-card outlined flat tile :href="file.file_url" target="_blank">
        <div class="icon">
          <v-icon class="icon" size="100px" color="orange darken-2">mdi-file</v-icon>
        </div>
      </v-card>
      <v-card-actions>
        <span class="file-name text-truncate">{{ file.name }}</span>
        <v-spacer></v-spacer>
        <v-btn icon>
          <v-icon>mdi-delete</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>mdi-share-variant</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-hover>
</template>

<script>
export default {
  props: {
    file: Object,
  },
};
</script>

<style lang="scss" scoped>
.icon {
  text-align: center;
}

.file-name {
  width: 80%;
  padding: 0px 0px 0px 12px;
}
</style>