<template>
  <v-app>
    <v-container fill-height justify-center align-center>
      <v-card color="blue lighten-2" class="login-card" width="500">
        <v-card-title>
          <span class="headline">Sign In</span>
        </v-card-title>

        <v-divider />
        <v-spacer />

        <v-card-text>
          <v-layout row fill-height justify-center align-center v-if="loading">
            <v-progress-circular :size="50" color="primary" indeterminate />
          </v-layout>

          <v-form v-else ref="form" v-model="valid" lazy-validation>
            <v-container>
              <v-text-field
                v-model="credentials.username"
                :counter="70"
                label="ユーザー名"
                :rules="rules.username"
                maxlength="70"
                required
              />

              <v-text-field
                type="password"
                v-model="credentials.password"
                :counter="20"
                label="パスワード"
                :rules="rules.password"
                maxlength="20"
                required
              />
            </v-container>
            <div>
              <v-btn text :disabled="!valid" @click="login">Login</v-btn>
            </div>
          </v-form>
        </v-card-text>
      </v-card>
    </v-container>
  </v-app>
</template>


<script>
export default {
  middleware: "auth",
  data: () => ({
    credentials: {},
    valid: true,
    loading: false,
    rules: {
      username: [(v) => !!v || "ユーザー名は必須です"],
      password: [(v) => !!v || "パスワードは必須です"],
    },
  }),
  methods: {
    async login() {
      try {
        await this.$auth.loginWith("local", { data: this.credentials });
      } catch (err) {
        console.log(err);
      }
    },
  },
};
</script>


