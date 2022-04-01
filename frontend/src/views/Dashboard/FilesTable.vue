<template>

  <b-card body-class="p-0" header-class="border-0">
    <template v-slot:header>
      <b-row align-v="center">
        <b-col>
          <h3 class="mb-0">{{ typeTr }}</h3>
        </b-col>
        <b-col class="text-right">
          <router-link :to="'/' + type" class="btn btn-sm btn-primary">Voir tout</router-link>
        </b-col>
      </b-row>
    </template>


    <div class="custom-loader">
      <i v-if="!loaded" class="fas fa-spinner fa-spin"></i>
    </div>

    <el-table v-if="loaded" class="table-responsive table"
              :data="tableData"
              header-row-class-name="thead-light">
      <el-table-column label="Nom"
                       min-width="70px"
                       prop="name">
        <template v-slot="{row}">
          <router-link class="text-reset" :to="'/file/'+ row.id">
            <div class="font-weight-600">{{ row.name }}</div>
          </router-link>
        </template>
      </el-table-column>

      <el-table-column label="Date"
                       min-width="70px"
                       prop="date">
        <template v-slot="{row}">
          {{ getDate(row.date) }}
        </template>
      </el-table-column>
    </el-table>
  </b-card>
</template>
<script>
import { Table, TableColumn, DropdownMenu, DropdownItem, Dropdown } from 'element-ui'
import axios from '@/plugins/axios'
import { format, utcToZonedTime } from "date-fns-tz";
import fr from "date-fns/locale/fr";

export default {
  name: 'page-visits-table',
  components: {
    [Table.name]: Table,
    [TableColumn.name]: TableColumn,
    [Dropdown.name]: Dropdown,
    [DropdownItem.name]: DropdownItem,
    [DropdownMenu.name]: DropdownMenu,
  },
  props: ['type'],
  data() {
    return {
      tableData: [],
      loaded: false
    }
  },
  created() {
    const params = { type: this.type }
    params['limit'] = 5
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
      const timeZoned = utcToZonedTime(date, 'Europe/Paris');
      return format(timeZoned, 'dd/MM/yyyy HH:mm', {
        locale: fr
      })
    }
  },
  computed: {
    typeTr() {
      return this.type === 'CV' ? 'Derniers CV' : 'Dernières Factures'
    }
  }
}
</script>
<style>
</style>
