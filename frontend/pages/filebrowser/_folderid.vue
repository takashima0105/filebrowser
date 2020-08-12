<template>
  <v-app>
    <v-main>
      <SnackBar
        ref="snackbar"
        :message="snackbar_props.message"
        :snack_color="snackbar_props.snack_color"
        :snackbar_close="SnackBarClose"
      />
      <AppBar :links="links" />
      <div class="file-upload" @dragenter.prevent="dragEnter">
        <v-container>
          <v-row>
            <v-col>
              <BreadCrumbs :breadcrumbs="breadcrumbs" />
            </v-col>
          </v-row>
          <v-row>
            <v-spacer />
            <FuncButton :text="'フォルダ追加'" :clickFunc="DialogDisplay" />
          </v-row>
          <v-row>
            <v-col xs="12" sm="4" md="2" v-for="(item, index) in items" v-bind:key="index">
              <FolderItem v-if="item.type === 'folder'" :folder="item.data" />
              <FileItem v-if="item.type === 'file'" :file="item.data" />
            </v-col>
          </v-row>
        </v-container>
      </div>
      <template v-if="isVisible">
        <div
          @dragleave.prevent="dragLeave"
          @dragover.prevent
          @drop.prevent="dropFile"
          class="overlay"
        ></div>
      </template>

      <Dialog ref="dialog" :width="300">
        <v-card>
          <v-card-title>フォルダの新規作成</v-card-title>
          <v-divider />
          <v-card-text class="pt-5">
            <span>フォルダ名</span>
            <v-text-field v-model="new_foldername" />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <FuncButton
              :text="'close'"
              :color="'error'"
              :textonly="true"
              :clickFunc="DialogNonDisplay"
            />
            <FuncButton :text="'create'" :textonly="true" :clickFunc="CreateFolder" />
          </v-card-actions>
        </v-card>
      </Dialog>

      <v-footer app fixed>
        <div class="pagination">
          <v-pagination v-model="page" :length="Math.ceil(count / 12)"></v-pagination>
        </div>
      </v-footer>
    </v-main>
  </v-app>
</template>

<script>
import AppBar from "~/components/common/AppBar.vue";
import FolderItem from "~/components/filebrowser/FolderItem.vue";
import FileItem from "~/components/filebrowser/FileItem.vue";
import BreadCrumbs from "~/components/common/BreadCrumbs.vue";
import FuncButton from "~/components/common/FuncButton.vue";
import Dialog from "~/components/common/Dialog.vue";
import SnackBar from "~/components/common/SnackBar.vue";
import { isNull } from "util";

export default {
  data() {
    return {
      user: this.$auth.user[0],
      links: [
        {
          text: "ファイルブラウザ",
          color: "white",
          url: "/filebrowser/",
          icon: "mdi-home",
          textonly: true,
          exact: false,
          disabled: false,
        },
      ],
      page: 1,
      limit: 12,
      new_foldername: "",
      snackbar_props: {
        timeout: 20000,
        message: "",
        snack_color: "info",
      },
      timeout_timer: Function,
      isVisible: false,
    };
  },

  async asyncData({ app, error, params }) {
    // フォルダリストの取得
    const folderlist_url = "/item/" + params.folderid + "/";
    const folderlist_response = await app.$axios
      .get(folderlist_url)
      .catch(function (err) {
        error({
          statusCode: err.response.status,
          message: err.response.data.message,
        });
        return err.response;
      });

    // パンくずリストの取得
    const breadcrumbs_url = "/breadcrumbs/" + params.folderid + "/";
    const breadcrumbs_response = await app.$axios.get(breadcrumbs_url);

    // パンくずリストの作成
    const breadcrumbs = new Array();
    if (isNull(breadcrumbs_response.data)) {
      breadcrumbs.push({
        text: "home",
        disabled: false,
        to: "/filebrowser/home",
      });
    } else {
      breadcrumbs_response.data.forEach(function (item, index) {
        breadcrumbs.push({
          text: item.name,
          disabled: false,
          to: "/filebrowser/" + item.id,
        });
      });

      breadcrumbs.unshift({
        text: "home",
        disabled: false,
        to: "/filebrowser/home",
      });
    }

    // 最後の要素のdisabledをtrueに変更する
    breadcrumbs[breadcrumbs.length - 1].disabled = true;

    return {
      breadcrumbs: breadcrumbs,
      items: folderlist_response.data.results,
      count: folderlist_response.data.count,
    };
  },

  watch: {
    page: function () {
      this.GetFolderList(this.page);
      return;
    },
  },

  methods: {
    DialogDisplay() {
      this.$refs.dialog.open();
    },

    DialogNonDisplay() {
      this.new_foldername = "";
      this.$refs.dialog.close();
    },

    SnackBarOpen() {
      this.$refs.snackbar.open();
      this.timeout_timer = setTimeout(() => {
        this.SnackBarClose();
      }, this.snackbar_props.timeout);
    },

    SnackBarClose() {
      this.$refs.snackbar.close();
      clearTimeout(this.timeout_timer);
    },

    async GetFolderList(page) {
      const folderlist_url =
        "/item/" + this.$route.params.folderid + "/?page=" + page;
      const folderlist_response = await this.$axios.get(folderlist_url);
      this.items = folderlist_response.data.results;
      this.count = folderlist_response.data.count;
    },

    async CreateFolder() {
      if (this.new_foldername === "") {
        // スナックバーの非表示
        this.SnackBarClose();

        // スナックバーの表示
        this.snackbar_props = {
          timeout: 5000,
          message: "フォルダ名を入力してください。",
          snack_color: "info",
        };
        this.SnackBarOpen();
        return;
      }

      const form_data = {
        name: this.new_foldername,
      };

      const foldercreate_url =
        "/folder_create/" + this.$route.params.folderid + "/";

      const foldercreate_response = await this.$axios
        .post(foldercreate_url, form_data)
        .then((response) => {
          // ダイアログの非表示
          this.DialogNonDisplay();
          // フォルダリストの取得
          this.GetFolderList(1);

          // スナックバーの非表示
          this.SnackBarClose();

          // スナックバーの表示
          this.snackbar_props = {
            timeout: 5000,
            message: form_data.name + "　を作成しました。",
            snack_color: "success",
          };
          this.SnackBarOpen();
        })
        .catch((err) => {
          // ダイアログの非表示
          this.DialogNonDisplay();

          // スナックバーの非表示
          this.SnackBarClose();

          // スナックバーの表示
          this.snackbar_props = {
            timeout: 5000,
            message: err.response.data.message,
            snack_color: "error",
          };
          this.SnackBarOpen();
        });
    },

    dragEnter(event) {
      //ファイルではなく、html要素をドラッグしてきた時は処理を中止
      if (event.dataTransfer.types.includes("text/plain")) {
        return;
      }
      this.isVisible = true;
    },

    dragLeave() {
      this.isVisible = false;
    },

    dropFile($event) {
      // 表示を元に戻す
      this.dragLeave();

      // ファイルを取得
      const files = event.target.files
        ? event.target.files
        : event.dataTransfer.files;

      // ファイルが無い場合又は複数ある場合は、処理を中止する
      if (files.length !== 1) {
        // スナックバーの非表示
        this.SnackBarClose();

        // スナックバーの表示
        this.snackbar_props = {
          timeout: 5000,
          message: "アップロードファイルが不正です。",
          snack_color: "error",
        };
        this.SnackBarOpen();
        return;
      }
      // 送信ファイルを作成
      const form_data = new FormData();
      form_data.append("file", files[0]);

      // ファイルの送信
      this.SendDrawingFile(form_data);
    },

    async SendDrawingFile(data) {
      const fileupload_url =
        "/file_upload/" + this.$route.params.folderid + "/";
      const fileupload_response = await this.$axios
        .post(fileupload_url, data)
        .then((response) => {
          // フォルダリストの取得
          this.GetFolderList(1);

          // スナックバーの非表示
          this.SnackBarClose();

          // スナックバーの表示
          this.snackbar_props = {
            timeout: 5000,
            message: response.data.name + "　をアップロードしました。",
            snack_color: "success",
          };
          this.SnackBarOpen();
        })
        .catch((err) => {
          // スナックバーの非表示
          this.SnackBarClose();

          // スナックバーの表示
          this.snackbar_props = {
            timeout: 5000,
            message: err.response.data.message,
            snack_color: "error",
          };
          this.SnackBarOpen();
        });
    },
  },

  components: {
    AppBar: AppBar,
    FolderItem: FolderItem,
    FileItem: FileItem,
    BreadCrumbs: BreadCrumbs,
    FuncButton: FuncButton,
    Dialog: Dialog,
    SnackBar: SnackBar,
  },
};
</script>

<style lang="scss" scoped>
.pagination {
  margin-left: auto;
  margin-right: auto;
}

.overlay {
  position: fixed;
  top: 0;
  z-index: 100;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
}
</style>