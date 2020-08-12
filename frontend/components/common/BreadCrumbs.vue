<template>
  <v-breadcrumbs :items="breadcrumbs" large>
    <!-- <template v-slot:item="props">
      <v-breadcrumbs-item
        exact
        :disabled="props.item.disabled"
        :to="props.item.href"
        link
      >{{ props.item.text }}</v-breadcrumbs-item>
    </template>-->
  </v-breadcrumbs>
</template>

<script>
export default {
  props: {
    breadcrumbs: Array,
  },
};
</script>