<template>
  <b-form
    @submit.stop.prevent="uploadFiles"
    @reset="onReset"
    enctype="multipart/form-data"
    class="text-center"
  >
    <dropzone-file-upload v-model="files" multiple :key="componentKey"></dropzone-file-upload>
    <b-button type="submit" variant="primary" :disabled="loading">
      <i v-if="loading" class="fas fa-spinner fa-spin"></i>
      <span v-else>Envoyer</span>
    </b-button>
    <div class="mt-5 text-center font-weight-bold" v-if="status" v-html="status"></div>
  </b-form>
</template>
<script>
import axios from "../../plugins/axios";
import DropzoneFileUpload from '@/components/Inputs/DropzoneFileUpload'

export default {
  components: {
    DropzoneFileUpload
  },
  data() {
    return {
      componentKey: 0,
      files: [],
      loading: false,
      status: ''
    };
  },
  methods: {
    uploadFiles() {
      this.status = ''
      const formData = new FormData();
      for (const i of Object.keys(this.files)) {
        formData.append('files', this.files[i])
      }
      this.loading = true
      axios.post(
        '/upload',
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      )
        .then(res => res.data)
        .then((data) => {
          this.loading = false
          this.onReset()
          this.status = `<div class="text-darker">Fichiers correctement uploadés</div><div>${data.uploaded}</div>`.replaceAll('invoice', 'Facture')
        })
        .catch(() => {
          this.loading = false
          this.status = `Une erreur est survenue`
        })
    },
    onReset() {
      this.files = [];
      this.componentKey += 1
    }
  }
};
</script>
