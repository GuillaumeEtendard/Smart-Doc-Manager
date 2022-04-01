import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}
import java.util.Properties

object kafkaProducer{

  def sendReport(topicarg : String = "images", key : Int, message : String): Unit = {
    val topic: String = topicarg
    val brokers: String = "localhost:29092"
    val props = new Properties()
    props.put("bootstrap.servers", brokers)
    props.put("client.id", "producer")
    props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    val producer = new KafkaProducer[String, String](props)
    val data = new ProducerRecord[String, String](topic, key.toString, message)
    producer.send(data)
    producer.close()
  }
}