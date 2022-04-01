<template>
  <div>
    <base-header class="pb-6 pb-8 pt-5 pt-md-8 bg-gradient-success d-flex align-items-center" style="min-height: 80vh">
      <b-row>
        <b-col>
          <file-upload/>
        </b-col>
      </b-row>
    </base-header>
  </div>
</template>
<script>
import FileUpload from "./Dashboard/FileUpload";

export default {
  components: {
    FileUpload
  },
  data() {
    return {};
  }
};
</script>
