<template>
  <b-card no-body>
    <b-card-header class="border-0">
      <h3 class="mb-0">{{ typeTr }}</h3>
    </b-card-header>

    <div class="custom-loader">
      <i v-if="!loaded" class="fas fa-spinner fa-spin"></i>
    </div>

    <el-table v-show="loaded" class="table-responsive table"
              header-row-class-name="thead-light"
              :data="tableData">
      <el-table-column label="Nom du fichier"
                       min-width="310px"
                       prop="name">
        <template v-slot="{row}">
          <router-link class="text-reset" :to="'/file/'+ row.id">
            <b-media no-body class="align-items-center">
              <span class="avatar bg-lighter rounded-circle mr-3">
                <i v-if="type === 'CV'" class="fa fa-address-book text-blue"></i>
                <i v-if="type === 'invoice'" class="fa fa-receipt text-dark"></i>
              </span>
              <b-media-body>
                <span class="font-weight-600 name mb-0 text-sm">{{ row.name }}</span>
              </b-media-body>
            </b-media>
          </router-link>
        </template>
      </el-table-column>

      <el-table-column label="Date"
                       min-width="150px"
                       prop="date">
        <template v-slot="{row}">
          {{ getDate(row.date) }}
        </template>
      </el-table-column>


      <el-table-column label="Données"
                       min-width="300px"
                       prop="data">
        <template v-slot="{row}">
          <div v-for="(data, idx) in JSON.parse(row.data).slice(0, 5)" :key="idx">
            {{ data }}
          </div>
        </template>
      </el-table-column>

    </el-table>

    <b-card-footer class="py-4 d-flex justify-content-end">
      <base-pagination v-model="currentPage" :per-page="100" :total="50"></base-pagination>
    </b-card-footer>
  </b-card>
</template>
<script>
import { format, utcToZonedTime } from 'date-fns-tz'
import fr from 'date-fns/locale/fr'

const timeZone = 'Europe/Paris';

import { Table, TableColumn } from 'element-ui'
import axios from "@/plugins/axios";

export default {
  name: 'light-table',
  components: {
    [Table.name]: Table,
    [TableColumn.name]: TableColumn
  },
  data() {
    return {
      tableData: [],
      currentPage: 1,
      loaded: false
    };
  },
  props: ['type'],
  created() {
    const params = { type: this.type }
    axios.get('/items', { params })
      .then(res => res.data)
      .then(data => {
        this.tableData = data
        this.loaded = true
      })
  },
  methods: {
    getDate(date) {
      date = date + 'Z'
      const timeZoned = utcToZonedTime(date, timeZone);
      return format(timeZoned, 'dd/MM/yyyy HH:mm', {
        locale: fr
      })
    },
    rowClicked(params) {
      console.log('click', params)
    }
  },
  computed: {
    typeTr() {
      return this.type === 'CV' ? 'CV' : 'Factures'
    }
  }
}
</script>
<style>
.custom-loader {
  text-align: center;
  font-size: 30px;
  color: #2b2b58;
}
</style>
