import kafka.utils.Logging
import org.apache.kafka.clients.consumer.{ConsumerConfig, ConsumerRecord, KafkaConsumer}
import org.apache.spark.sql.SparkSession
import java.time.Duration
import java.util.{Collections, Properties}
import scala.jdk.CollectionConverters._


class kafkaConsumer(val topic: String) extends Logging {
  val props: Properties = createConsumerConfig()
  val consumer = new KafkaConsumer[String, String](props)

  //consumer stream

  def createConsumerConfig(): Properties = {
    val props = new Properties()
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:29092")
    props.put(ConsumerConfig.GROUP_ID_CONFIG, "2")
    props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true")
    props.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, "1000")
    props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, "30000")
    props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer")
    props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer")
    props
  }

  def run_iterateIterator(iterator: Iterator[ConsumerRecord[String, String]]): Unit ={
    if (iterator.hasNext) {
      val report = iterator.next().value()
      println(report)
    }
    else {
      println("empty")
    }
  }

  def run(): Unit = {
    consumer.subscribe(Collections.singletonList(this.topic))
    val record = consumer.poll(Duration.ofMillis(1000)).asScala
    run_iterateIterator(record.iterator)
    run()
  }

  //consumer bash

  def readAll(offset_inferior : BigInt): Array[String] = {
    val spark = SparkSession
      .builder()
      .appName("infraSmartDoc")
      .config("spark.master", "local")
      .getOrCreate()

    import spark.implicits._

    val df = spark
      .read
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:29092")
      .option("subscribe", "test")
      .option("startingOffsets", s"""{"test":{"0":$offset_inferior}}""")
      .load()
    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
      .as[(String, String)]

    if (!df.isEmpty) {
      val array = df.select($"value".as[String]).collectAsList().toArray()
      spark.close()
      array.map(x => x.toString)
    }else{
      Array()
    }
  }

}

object kafkaConsumer {
  def kafkaConsumer(): Unit = {
    val streamReader = new kafkaConsumer( "test")
    streamReader.run()
  }
  def consumeAll(): Unit = {
    val streamReader = new kafkaConsumer("test")
    println("start")
    streamReader.readAll(0).foreach(elt => println(elt))
    println("end")

  }

}
