<template>
  <div
    class="dropzone mb-3 dz-clickable"
    :class="[multiple ? 'dropzone-multiple' : 'dropzone-single']"
  >
    <div class="dz-message" data-dz-message><span>Déposez vos fichiers ici</span></div>
    <div class="fallback">
      <div class="custom-file">
        <input
          id="projectCoverUploads"
          type="file"
          class="custom-file-input"
          :multiple="multiple"
        />
        <label class="custom-file-label" for="projectCoverUploads"
        >Choisir le(s) fichier(s)</label
        >
      </div>
    </div>
    <div
      v-if="!multiple"
      ref="previewSingle"
      class="dz-preview dz-preview-single"
      :class="previewClasses"
    >
      <div class="dz-preview-cover">
        <img class="dz-preview-img" data-dz-thumbnail />
      </div>
    </div>
    <ul
      v-else
      ref="previewMultiple"
      class="dz-preview dz-preview-multiple list-group list-group-lg list-group-flush"
      :class="previewClasses"
    >
      <li class="list-group-item px-0">
        <div class="row align-items-center pb-2">
          <div class="col ml-2">
            <h4 class="mb-1" data-dz-name>...</h4>
            <p class="small text-muted mb-0" data-dz-size>...</p>
          </div>
          <div class="col-auto mr-2">
            <button data-dz-remove="true" class="btn btn-danger btn-sm">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  name: 'DropzoneFileUpload',
  model: {
    prop: 'value',
    event: 'change',
  },
  props: {
    options: {
      type: Object,
      default: () => ({}),
    },
    value: {
      type: [String, Object, Array],
      default: null,
    },
    url: {
      type: String,
      default: 'http://',
    },
    multiple: Boolean,
    previewClasses: {
      type: [String, Object, Array],
      default: null,
    },
  },
  emits: ['change'],
  data() {
    return {
      currentFile: null,
      files: [],
      showList: false,
    };
  },
  async mounted() {
    this.initDropzone();
  },
  methods: {
    async initDropzone() {
      let Dropzone = await import('dropzone');
      Dropzone = Dropzone.default || Dropzone;
      Dropzone.autoDiscover = false;
      const preview = this.multiple
        ? this.$refs.previewMultiple
        : this.$refs.previewSingle;
      const self = this;
      const finalOptions = {
        ...this.options,
        url: this.url,
        thumbnailWidth: null,
        thumbnailHeight: null,
        previewsContainer: preview,
        previewTemplate: preview.innerHTML,
        maxFiles: !this.multiple ? 1 : null,
        acceptedFiles: !this.multiple ? 'image/*' : null,
        init() {
          this.on('addedfile', (file) => {
            if (!self.multiple && self.currentFile) {
              // this.removeFile(this.currentFile);
            }
            self.currentFile = file;
          });
        },
      };
      this.dropzone = new Dropzone(this.$el, finalOptions);
      preview.innerHTML = '';
      const evtList = [
        'drop',
        'dragstart',
        'dragend',
        'dragenter',
        'dragover',
        'addedfile',
        'removedfile',
        'thumbnail',
        'error',
        'processing',
        'uploadprogress',
        'sending',
        'success',
        'complete',
        'canceled',
        'maxfilesreached',
        'maxfilesexceeded',
        'processingmultiple',
        'sendingmultiple',
        'successmultiple',
        'completemultiple',
        'canceledmultiple',
        'totaluploadprogress',
        'reset',
        'queuecomplete',
      ];
      evtList.forEach((evt) => {
        this.dropzone.on(evt, (data) => {
          this.$emit(evt, data);
          if (evt === 'addedfile') {
            this.files.push(data);
            this.$emit('change', this.files);
          } else if (evt === 'removedfile') {
            const index = this.files.findIndex(
              (f) => f.upload.uuid === data.upload.uuid,
            );
            if (index !== -1) {
              this.files.splice(index, 1);
            }
            this.$emit('change', this.files);
          }
        });
      });
    },
  },
};
</script>
<style></style>
