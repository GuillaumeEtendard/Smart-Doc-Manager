<template>
  <div>
    <div>
      <base-header class="pb-6 pb-8 pt-5 pt-md-8 bg-gradient-success">
      </base-header>
      <b-container fluid class="mt--6">
        <b-row>
          <b-col xl="12" class="order-xl-2 mb-5">
            <b-card no-body class="card-profile" alt="Image placeholder" img-top>
              <b-card-header class="text-center border-0 pt-8 pt-md-4 pb-0 pb-md-4">
                <div class="d-flex justify-content-between">
                  <router-link :to="'/' + data.type" class="btn btn-sm btn-info mr-4">Revenir aux {{
                      typeTr
                    }}
                  </router-link>
                  <button @click="() => $router.go(0)" class="btn btn-sm btn-default float-right">Actualiser
                  </button>
                </div>
              </b-card-header>

              <b-card-body v-if="data" class="pt-0">
                <div class="text-center">
                  <h5 class="h3">
                    {{ data.name }}
                  </h5>
                  <div class="h5 font-weight-300">
                    <i class="fa fa-calendar mr-2"></i>{{ getDate(data.date) }}
                  </div>
                </div>
                <hr class="my-4">
                <div v-if="data.data">
                  <div v-for="(data, idx) in JSON.parse(data.data)" :key="idx">
                    {{ data }}
                  </div>
                </div>
              </b-card-body>
            </b-card>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>
<script>

import axios from "@/plugins/axios";
import { format, utcToZonedTime } from "date-fns-tz";
import fr from "date-fns/locale/fr";

export default {
  components: {},
  data() {
    return {
      data: {}
    }
  },
  async beforeRouteUpdate(to, from) {
    this.fetchFile(to.params.id)
  },
  created() {
    this.fetchFile(this.$route.params.id)
  },
  methods: {
    fetchFile(id) {
      axios.get(`/items/${id}`)
        .then(res => res.data)
        .then(data => {
          this.data = data
        })
    },
    getDate(date) {
      date = date + 'Z'
      const timeZoned = utcToZonedTime(date, 'Europe/Paris');
      return format(timeZoned, 'dd/MM/yyyy HH:mm', {
        locale: fr
      })
    }
  },
  computed: {
    typeTr() {
      if (this.data.type === 'CV')
        return 'CV'
      else if (this.data.type === 'invoice')
        return 'factures'
      else
        return ''
    }
  }
};
</script>
<style>
</style>
