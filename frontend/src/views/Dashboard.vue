<template>
  <div>
    <base-header class="pb-6 pb-8 pt-5 pt-md-8 bg-gradient-success">
      <!-- Card stats -->
      <b-row>
        <b-col xl="6" md="6">
          <stats-card
            title="Nombre de CV"
            type="gradient-red"
            :sub-title="`${dashboardData.totalCV}`"
            icon="fa fa-address-book"
            class="mb-4"
          >
          </stats-card>
        </b-col>
        <b-col xl="6" md="6">
          <stats-card
            title="Nombre de factures"
            type="gradient-orange"
            :sub-title="`${dashboardData.totalInvoice}`"
            icon="fa fa-receipt"
            class="mb-4"
          >
          </stats-card>
        </b-col>
      </b-row>
    </base-header>

    <b-container fluid class="mt--7">
      <!--Tables-->
      <b-row>
        <b-col xl="6" class="mb-5 mb-xl-0">
          <files-table type="CV"></files-table>
        </b-col>
        <b-col xl="6" class="mb-5 mb-xl-0">
          <files-table type="invoice"></files-table>
        </b-col>
      </b-row>

      <b-row class="mt-5">
        <b-col xl="12" class="mb-5 mb-xl-0">
          <card type="default" header-classes="bg-transparent">
            <b-row align-v="center" slot="header">
              <b-col>
                <h6 class="text-light text-uppercase ls-1 mb-1">2022</h6>
                <h5 class="h3 text-white mb-0">Fichiers mis en ligne</h5>
              </b-col>
            </b-row>
            <line-chart
              :height="350"
              ref="bigChart"
              :chart-data="bigLineChart.chartData"
              :extra-options="bigLineChart.extraOptions"
            >
            </line-chart>
          </card>
        </b-col>
      </b-row>

      <!--End tables-->
    </b-container>
  </div>
</template>
<script>
// Charts
import * as chartConfigs from "@/components/Charts/config";
import LineChart from "@/components/Charts/LineChart";
import BarChart from "@/components/Charts/BarChart";

// Components
import BaseProgress from "@/components/BaseProgress";
import StatsCard from "@/components/Cards/StatsCard";

// Tables
import FilesTable from "./Dashboard/FilesTable";
import FileUpload from "./Dashboard/FileUpload";

import axios from "@/plugins/axios";

export default {
  components: {
    LineChart,
    BarChart,
    BaseProgress,
    StatsCard,
    FilesTable,
    FileUpload
  },
  data() {
    return {
      dashboardData: {},
      bigLineChart: {
        allData: [
          [],
        ],
        chartData: {
          datasets: [
            {
              label: "Fichiers",
              data: [],
            },
          ],
          labels: [],
        },
        extraOptions: chartConfigs.blueChartOptions,
      }
    };
  },
  methods: {
    initBigChart(data) {
      let chartData = {
        datasets: [
          {
            label: "Fichiers",
            data: data.months_values,
          },
        ],
        labels: data.months_names,
      };
      this.bigLineChart.chartData = chartData;
    },
  },
  mounted() {
  },
  created() {
    axios.get('/dashboard')
      .then(res => res.data)
      .then(data => {
        this.dashboardData = data
        this.initBigChart(data);
      })
  }
};
</script>
<style>
.el-table .cell {
  padding-left: 0px;
  padding-right: 0px;
}
</style>
